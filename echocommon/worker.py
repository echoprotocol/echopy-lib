# -*- coding: utf-8 -*-
from .exceptions import WorkerDoesNotExistsException
from .utils import formatTimeString
from .blockchainobject import BlockchainObject, BlockchainObjects
from .instance import AbstractBlockchainInstanceProvider


class Worker(BlockchainObject, AbstractBlockchainInstanceProvider):
    """ Read data about a worker in the chain

        :param str id: id of the worker
        :param instance blockchain_instance: instance to use when accesing a RPC

    """

    def __init__(self, *args, **kwargs):
        self.define_classes()
        assert self.account_class
        assert self.type_id
        BlockchainObject.__init__(self, *args, **kwargs)
        self.post_format()

    def post_format(self):
        if isinstance(self["work_end_date"], str):
            self["work_end_date"] = formatTimeString(self["work_end_date"])
            self["work_begin_date"] = formatTimeString(self["work_begin_date"])
        self["daily_pay"] = int(self["daily_pay"])

    def refresh(self):
        worker = self.blockchain.rpc.get_object(self.identifier)
        if not worker:
            raise WorkerDoesNotExistsException
        super(Worker, self).__init__(worker, blockchain_instance=self.blockchain)
        self.post_format()

    @property
    def account(self):
        return self.account_class(
            self["worker_account"], blockchain_instance=self.blockchain
        )


class Workers(BlockchainObjects, AbstractBlockchainInstanceProvider):
    """ Obtain a list of workers for an account

        :param str account_name/id: Name/id of the account (optional)
        :param instance blockchain_instance: instance to use when accesing a RPC
    """

    def __init__(self, *args, account_name=None, lazy=False, **kwargs):
        self.define_classes()
        assert self.account_class
        assert self.worker_class

        self.account_name = account_name
        self.lazy = lazy
        super().__init__(*args, **kwargs)

    def refresh(self, *args, **kwargs):
        if self.account_name:
            account = self.account_class(
                self.account_name, blockchain_instance=self.blockchain
            )
            self.workers = self.blockchain.rpc.get_workers_by_account(account["id"])
        else:
            self.workers = self.blockchain.rpc.get_all_workers()

        self.store(
            [
                self.worker_class(
                    x, lazy=self.lazy, blockchain_instance=self.blockchain
                )
                for x in self.workers
            ]
        )
