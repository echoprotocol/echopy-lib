from .echoapi import Api
from .transaction import Transaction
from .echobase.config import Config
from .echobase.account import BrainKey


class Echo:

    def __init__(self):
        self.api = Api()
        self.config = Config()
        self.brain_key = BrainKey

    def create_transaction(self):
        return Transaction(self.api)

    def connect(self, url):
        self.api.connect(url)

    def disconnect(self):
        self.api.disconnect()
