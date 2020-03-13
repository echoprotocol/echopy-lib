#: api-config
class ApiConfig:
    def __init__(self):
        self.lookup_accounts_default_limit = 100
        self.lookup_accounts_max_limit = 1000

        self.list_assets_default_limit = 10
        self.list_assets_max_limit = 1000

        self.get_trade_history_default_limit = 10
        self.get_trade_history_max_limit = 100

        self.lookup_witness_accounts_default_limit = 100
        self.lookup_witness_accounts_max_limit = 1000

        self.commitee_member_accounts_default_limit = 100
        self.commitee_member_accounts_max_limit = 1000

        self.account_history_default_limit = 100
        self.account_history_max_limit = 100

        self.relative_account_history_default_limit = 100
        self.relative_account_history_max_limit = 100

        self.relative_account_history_start = 0
        self.relative_account_history_stop = 0

        self.account_history_operations_default_limit = 100
        self.account_history_operations_max_limit = 100

        self.contract_history_default_limit = 100
        self.contract_history_max_limit = 100

        self.order_book_default_depth = 50
        self.order_book_max_depth = 50

        self.start_operation_history_id = '1.10.0'
        self.stop_operation_history_id = '1.10.0'

        self.expiration_max_lag_seconds = 30
