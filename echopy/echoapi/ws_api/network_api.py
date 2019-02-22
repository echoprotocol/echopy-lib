class NetworkApi:
    def __init__(self, db):
        self.db = db

    def broadcast_transaction(self, signed_transaction):
        return self.db.rpcexec('broadcast_transaction', [signed_transaction])

    def broadcast_block(self, signed_block):
        return self.db.rpcexec('broadcast_block', [signed_block])

    def broadcast_transaction_synchronous(self, signed_transaction):
        return self.db.rpcexec('broadcast_transaction_synchronous', [signed_transaction])

    def broadcast_transaction_with_callback(self, signed_transaction, callback):
        return self.db.rpcexec('broadcast_transaction_with_callback', [callback, signed_transaction])
