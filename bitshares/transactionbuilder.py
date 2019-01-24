# -*- coding: utf-8 -*-
from graphenecommon.transactionbuilder import (
    TransactionBuilder as GrapheneTransactionBuilder,
    ProposalBuilder as GrapheneProposalBuilder,
)

from bitsharesbase import operations, transactions
from bitsharesbase.account import PrivateKey, PublicKey
from bitsharesbase.objects import Operation
from bitsharesbase.signedtransactions import Signed_Transaction

from .amount import Amount
from .asset import Asset
from .account import Account
from .instance import BlockchainInstance


@BlockchainInstance.inject
class ProposalBuilder(GrapheneProposalBuilder):
    """ Proposal Builder allows us to construct an independent Proposal
        that may later be added to an instance ot TransactionBuilder

        :param str proposer: Account name of the proposing user
        :param int proposal_expiration: Number seconds until the proposal is
            supposed to expire
        :param int proposal_review: Number of seconds for review of the
            proposal
        :param .transactionbuilder.TransactionBuilder: Specify
            your own instance of transaction builder (optional)
        :param instance blockchain_instance: Blockchain instance
    """

    def define_classes(self):
        self.operation_class = Operation
        self.operations = operations
        self.account_class = Account


@BlockchainInstance.inject
class TransactionBuilder(GrapheneTransactionBuilder):
    """ This class simplifies the creation of transactions by adding
        operations and signers.
    """

    def define_classes(self):
        self.account_class = Account
        self.asset_class = Asset
        self.operation_class = Operation
        self.operations = operations
        self.privatekey_class = PrivateKey
        self.publickey_class = PublicKey
        self.signed_transaction_class = Signed_Transaction
        self.amount_class = Amount
        self.counter = 0

    def broadcast(self):
        """ Broadcast a transaction to the blockchain network

            :param tx tx: Signed transaction to broadcast
        """
        # Cannot broadcast an empty transaction

        if not self._is_signed():
            self.sign()

        if "operations" not in self or not self["operations"]:
            return

        ret = self.json()

        if self.blockchain.nobroadcast:
            # log.warning("Not broadcasting anything!")
            self.clear()
            return ret

        # Broadcast
        try:

            new_ret = self.blockchain.rpc.broadcast_transaction_with_callback(self.counter, ret, api="network_broadcast")
            self.counter += 1
            print(self.counter)
            if new_ret:
                ret = new_ret
            '''
            if self.blockchain.blocking:
                ret = self.blockchain.rpc.broadcast_transaction_synchronous(
                    ret, api="network_broadcast"
                )
                ret.update(**ret.get("trx", {}))
            else:
                self.blockchain.rpc.broadcast_transaction(ret, api="network_broadcast")
            '''
        except Exception as e:
            raise e
        finally:
            self.clear()

        return ret
