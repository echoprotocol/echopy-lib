# -*- coding: utf-8 -*-
import logging

from .blockchainobject import BlockchainObject
from .exceptions import AccountDoesNotExistsException
from .instance import AbstractBlockchainInstanceProvider


log = logging.getLogger()


class Account(BlockchainObject, AbstractBlockchainInstanceProvider):
    """ This class allows to easily access Account data

        :param str account_name: Name of the account
        :param instance blockchain_instance: instance to use when accesing a RPC
        :param bool full: Obtain all account data including orders, positions, etc.
        :param bool lazy: Use lazy loading
        :param bool full: Obtain all account data including orders, positions,
               etc.
        :returns: Account data
        :rtype: dictionary
        :raises .exceptions.AccountDoesNotExistsException: if account
                does not exist

        Instances of this class are dictionaries that come with additional
        methods (see below) that allow dealing with an account and it's
        corresponding functions.

        .. code-block:: python

            from .account import Account
            account = Account("init0")
            print(account)

        .. note:: This class comes with its own caching function to reduce the
                  load on the API server. Instances of this class can be
                  refreshed with ``Account.refresh()``.

    """

    def __init__(self, *args, **kwargs):
        self.define_classes()
        assert self.type_id
        assert self.amount_class
        assert self.operations

        self.full = kwargs.pop("full", False)
        BlockchainObject.__init__(self, *args, **kwargs)

    def refresh(self):
        """ Refresh/Obtain an account's data from the API server
        """
        import re

        if re.match(r"^1\.2\.[0-9]*$", self.identifier):
            account = self.blockchain.rpc.get_objects([self.identifier])[0]
        else:
            account = self.blockchain.rpc.lookup_account_names([self.identifier])[0]
        if not account:
            raise AccountDoesNotExistsException(self.identifier)
        self.store(account, "name")

        if self.full:
            accounts = self.blockchain.rpc.get_full_accounts([account["id"]], False)
            if accounts and isinstance(accounts, list):
                account = accounts[0][1]
            else:
                raise AccountDoesNotExistsException(self.identifier)
            super(Account, self).__init__(
                account["account"], blockchain_instance=self.blockchain
            )
            for k, v in account.items():
                if k != "account":
                    self[k] = v
        else:
            super(Account, self).__init__(account, blockchain_instance=self.blockchain)

    @property
    def name(self):
        return self["name"]

    @property
    def is_fully_loaded(self):
        """ Is this instance fully loaded / e.g. all data available?
        """
        return self.full and "votes" in self

    def ensure_full(self):
        if not self.is_fully_loaded:
            self.full = True
            self.refresh()

    @property
    def is_ltm(self):
        """ Is the account a lifetime member (LTM)?
        """
        return self.get("id") == self.get("lifetime_referrer")

    @property
    def balances(self):
        """ List balances of an account. This call returns instances of
            :class:`amount.Amount`.
        """
        balances = self.blockchain.rpc.get_account_balances(self["id"], [])
        return [
            self.amount_class(b, blockchain_instance=self.blockchain)
            for b in balances
            if int(b["amount"]) > 0
        ]

    def balance(self, symbol):
        """ Obtain the balance of a specific Asset. This call returns instances of
            :class:`amount.Amount`.
        """
        if isinstance(symbol, dict) and "symbol" in symbol:
            symbol = symbol["symbol"]
        balances = self.balances
        for b in balances:
            if b["symbol"] == symbol:
                return b
        return self.amount_class(0, symbol)

    def history(self, first=0, last=0, limit=-1, only_ops=[], exclude_ops=[]):
        """ Returns a generator for individual account transactions. The
            latest operation will be first. This call can be used in a
            ``for`` loop.

            :param int first: sequence number of the first
                transaction to return (*optional*)
            :param int last: sequence number of the last
                transaction to return (*optional*)
            :param int limit: limit number of transactions to
                return (*optional*)
            :param array only_ops: Limit generator by these
                operations (*optional*)
            :param array exclude_ops: Exclude these operations from
                generator (*optional*).

            ... note::
                only_ops and exclude_ops takes an array of strings:
                The full list of operation ID's can be found in
                operationids.py.
                Example: ['transfer', 'fill_order']
        """
        _limit = 100
        cnt = 0

        if first < 0:
            first = 0

        while True:
            # RPC call
            txs = self.blockchain.rpc.get_account_history(
                self["id"],
                "1.11.{}".format(last),
                _limit,
                "1.11.{}".format(first - 1),
                api="history",
            )
            for i in txs:
                if (
                    exclude_ops
                    and self.operations.getOperationNameForId(i["op"][0]) in exclude_ops
                ):
                    continue
                if (
                    not only_ops
                    or self.operations.getOperationNameForId(i["op"][0]) in only_ops
                ):
                    cnt += 1
                    yield i
                    if limit >= 0 and cnt >= limit:
                        return

            if not txs:
                log.info("No more history returned from API node")
                break
            if len(txs) < _limit:
                log.info("Less than {} have been returned.".format(_limit))
                break
            first = int(txs[-1]["id"].split(".")[2])

    def upgrade(self):
        """ Upgrade account to life time member
        """
        assert callable(self.blockchain.upgrade_account)
        return self.blockchain.upgrade_account(account=self)

    def whitelist(self, account):
        """ Add an other account to the whitelist of this account
        """
        assert callable(self.blockchain.account_whitelist)
        return self.blockchain.account_whitelist(account, lists=["white"], account=self)

    def blacklist(self, account):
        """ Add an other account to the blacklist of this account
        """
        assert callable(self.blockchain.account_whitelist)
        return self.blockchain.account_whitelist(account, lists=["black"], account=self)

    def nolist(self, account):
        """ Remove an other account from any list of this account
        """
        assert callable(self.blockchain.account_whitelist)
        return self.blockchain.account_whitelist(account, lists=[], account=self)


class AccountUpdate(dict, AbstractBlockchainInstanceProvider):
    """ This purpose of this class is to keep track of account updates
        as they are pushed through by :class:`notify.Notify`.

        Instances of this class are dictionaries and take the following
        form:

        ... code-block: js

            {'id': '2.6.29',
             'lifetime_fees_paid': '44261516129',
             'most_recent_op': '2.9.0',
             'owner': '1.2.29',
             'pending_fees': 0,
             'pending_vested_fees': 16310,
             'total_core_in_orders': '6788845277634',
             'total_ops': 0}

    """

    def __init__(self, data, *args, **kwargs):
        self.define_classes()
        assert self.account_class
        if isinstance(data, dict):
            super(AccountUpdate, self).__init__(data)
        else:
            account = self.account_class(data, blockchain_instance=self.blockchain)
            update = self.blockchain.rpc.get_objects(
                ["2.6.%s" % (account["id"].split(".")[2])]
            )[0]
            super(AccountUpdate, self).__init__(update)

    @property
    def account(self):
        """ In oder to obtain the actual
            :class:`account.Account` from this class, you can
            use the ``account`` attribute.
        """
        account = self.account_class(self["owner"], blockchain_instance=self.blockchain)
        # account.refresh()
        return account

    def __repr__(self):
        return "<AccountUpdate: {}>".format(self["owner"])
