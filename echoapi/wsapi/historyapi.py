# -*- coding: utf-8 -*-

START_OPERATION_ID = 0
# FIXED


class HistoryAPI:

    def __init__(self, connection):
        self.connection = connection

    def get_account_history(self, account_id, stop=START_OPERATION_ID, limit=100, start=START_OPERATION_ID):
        return self.connection.rpcexec('get_account_history', [account_id, stop, limit, start])

    def get_relative_account_history(self, account_id, stop=0, limit=100, start=0):
        return self.connection.rpcexec('get_relative_account_history', [account_id, stop, limit, start])

    def get_account_history_operations(self, account_id, operation_id, start=START_OPERATION_ID, stop=START_OPERATION_ID, limit=100):
        return self.connection.rpcexec('get_account_history_operations', [account_id, operation_id, start, stop, limit])

    def get_contract_history(self, contract_id, stop=START_OPERATION_ID, limit=100, start=START_OPERATION_ID):
        return self.connection.rpcexec('get_contract_history', [contract_id, stop, limit, start])
