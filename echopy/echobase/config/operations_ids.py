#: operations_ids
class OperationIds:
    def __init__(self):
        self.TRANSFER = 0
        self.LIMIT_ORDER_CREATE = 1
        self.LIMIT_ORDER_CANCEL = 2
        self.CALL_ORDER_UPDATE = 3
        self.FILL_ORDER = 4
        self.ACCOUNT_CREATE = 5
        self.ACCOUNT_UPDATE = 6
        self.ACCOUNT_WHITELIST = 7
        self.ACCOUNT_UPGRADE = 8
        self.ACCOUNT_TRANSFER = 9
        self.ASSET_CREATE = 10
        self.ASSET_UPDATE = 11
        self.ASSET_UPDATE_BITASSET = 12
        self.ASSET_UPDATE_FEED_PRODUCERS = 13
        self.ASSET_ISSUE = 14
        self.ASSET_RESERVE = 15
        self.ASSET_FUND_FEE_POOL = 16
        self.ASSET_SETTLE = 17
        self.ASSET_GLOBAL_SETTLE = 18
        self.ASSET_PUBLISH_FEED = 19
        self.PROPOSAL_CREATE = 20
        self.PROPOSAL_UPDATE = 21
        self.PROPOSAL_DELETE = 22
        self.WITHDRAW_PERMISSION_CREATE = 23
        self.WITHDRAW_PERMISSION_UPDATE = 24
        self.WITHDRAW_PERMISSION_CLAIM = 25
        self.WITHDRAW_PERMISSION_DELETE = 26
        self.COMMITTEE_MEMBER_CREATE = 27
        self.COMMITTEE_MEMBER_UPDATE = 28
        self.COMMITTEE_MEMBER_UPDATE_GLOBAL_PARAMETERS = 29
        self.VESTING_BALANCE_CREATE = 30
        self.VESTING_BALANCE_WITHDRAW = 31
        self.CUSTOM = 32
        self.ASSERT = 33
        self.BALANCE_CLAIM = 34
        self.OVERRIDE_TRANSFER = 35
        self.ASSET_SETTLE_CANCEL = 36
        self.ASSET_CLAIM_FEES = 37
        self.BID_COLLATERAL = 38
        self.EXECUTE_BID = 39
        self.CREATE_CONTRACT = 40
        self.CALL_CONTRACT = 41
        self.CONTRACT_TRANSFER = 42
