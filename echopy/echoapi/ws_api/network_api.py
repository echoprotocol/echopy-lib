class NetworkApi:
    def __init__(self, db):
        self.db = db

    async def broadcast_transaction(self, trx):
        return await self.db.rpcexec(
            'broadcast_transaction',
            [trx]
        )

    async def broadcast_block(self, signed_block):
        return await self.db.rpcexec(
            'broadcast_block',
            [signed_block]
        )

    async def broadcast_transaction_synchronous(self, trx):
        return await self.db.rpcexec(
            'broadcast_transaction_synchronous',
            [trx]
        )

    async def broadcast_transaction_with_callback(self, trx, cb):
        return await self.db.rpcexec(
            'broadcast_transaction_with_callback',
            [cb, trx]
        )
