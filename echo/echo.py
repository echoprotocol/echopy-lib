import logging

from echoapi import Api

from echobase import operations

from echobase.account import PublicKey

from .transaction import Transaction


log = logging.getLogger(__name__)


class Echo:

    def __init__(self, node):
        self.api = Api(node)

    def create_transaction(self):
        return Transaction(self.api)
