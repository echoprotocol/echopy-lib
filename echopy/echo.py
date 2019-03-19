from .echoapi import Api
from .transaction import Transaction
from .echobase.config import Config

class Echo:

    def __init__(self):
        self.api = Api()
        self.config = Config()

    def create_transaction(self):
        return Transaction(self.api)

    async def connect(self, url):
        await self.api.connect(url)

    async def disconnect(self):
        await self.api.disconnect()
