class NetworkApi:
    def __init__(self, db):
        self.db = db

    async def broadcast_transaction(self, signed_transaction):
        return await self.db.rpcexec('broadcast_transaction', [signed_transaction])

    async def broadcast_block(self, signed_block):
        return await self.db.rpcexec('broadcast_block', [signed_block])

    async def broadcast_transaction_synchronous(self, signed_transaction):
        return await self.db.rpcexec('broadcast_transaction_synchronous', [signed_transaction])

    async def broadcast_transaction_with_callback(self, signed_transaction, callback):
        return await self.db.rpcexec('broadcast_transaction_with_callback', [callback, signed_transaction])
