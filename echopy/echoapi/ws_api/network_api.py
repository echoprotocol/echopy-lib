class NetworkApi:
    def __init__(self, db):
        self.db = db

    def broadcast_transaction(self, trx):
        return self.db.rpcexec(
            'broadcast_transaction',
            [trx]
        )

    def broadcast_block(self, signed_block):
        return self.db.rpcexec(
            'broadcast_block',
            [signed_block]
        )

    def broadcast_transaction_synchronous(self, trx):
        return self.db.rpcexec(
            'broadcast_transaction_synchronous',
            [trx]
        )

    def broadcast_transaction_with_callback(self, trx, cb):
        return self.db.rpcexec(
            'broadcast_transaction_with_callback',
            [cb, trx]
        )
