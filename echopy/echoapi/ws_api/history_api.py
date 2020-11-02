class HistoryApi:
    def __init__(self, db):
        self.db = db

    def get_account_history(self, account, stop='1.6.0', limit=100, start='1.6.0'):
        return self.db.rpcexec(
            'get_account_history',
            [account, stop, limit, start]
        )

    def get_relative_account_history(self, account, stop=0, limit=100, start=0):
        return self.db.rpcexec(
            'get_relative_account_history',
            [account, stop, limit, start]
        )

    def get_account_history_operations(self, account, operation_id, start='1.6.0', stop='1.6.0', limit=100):
        return self.db.rpcexec(
            'get_account_history_operations',
            [account, operation_id, start, stop, limit]
        )

    def get_contract_history(self, contract, stop='1.6.0', limit=100, start='1.6.0'):
        return self.db.rpcexec(
            'get_contract_history',
            [contract, stop, limit, start]
        )

    def get_relative_contract_history(self, contract, stop=0, limit=100, start=0):
        return self.db.rpcexec(
            'get_relative_contract_history',
            [contract, stop, limit, start]
        )
     
    def get_account_address_history(self, address, start='1.6.0', stop='1.6.0', limit=100):
        return self.db.rpcexec(
            'get_account_address_history',
            [address, start, stop, limit]
        )
