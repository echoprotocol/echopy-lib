class HistoryApi:
    def __init__(self, db):
        self.db = db

    def get_account_history(self, account_id, stop="1.10.0", limit=100, start="1.10.0"):
        return self.db.rpcexec('get_account_history', [account_id, stop, limit, start])

    def get_relative_account_history(self, account_id, stop=0, limit=100, start=0):
        return self.db.rpcexec('get_relative_account_history', [account_id, stop, limit, start])

    def get_account_history_operations(self, account_id, operation_id, stop="1.10.0", limit=100, start="1.10.0"):
        return self.db.rpcexec('get_account_history_operations', [account_id, operation_id, start, stop, limit])

    def get_contract_history(self, contract_id, stop="1.10.0", limit=100, start="1.10.0"):
        return self.db.rpcexec('get_contract_history', [contract_id, stop, limit, start])
