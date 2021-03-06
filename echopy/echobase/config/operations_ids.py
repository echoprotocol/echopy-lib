#: operations_ids
class OperationIds:
    def __init__(self):
        self.TRANSFER = 0
        self.TRANSFER_TO_ADDRESS = 1
        self.OVERRIDE_TRANSFER = 2
        self.ACCOUNT_CREATE = 3
        self.ACCOUNT_UPDATE = 4
        self.ACCOUNT_WHITELIST = 5
        self.ACCOUNT_ADDRESS_CREATE = 6
        self.ASSET_CREATE = 7
        self.ASSET_UPDATE = 8
        self.ASSET_UPDATE_BITASSET = 9
        self.ASSET_UPDATE_FEED_PRODUCERS = 10
        self.ASSET_ISSUE = 11
        self.ASSET_RESERVE = 12
        self.ASSET_FUND_FEE_POOL = 13
        self.ASSET_PUBLISH_FEED = 14
        self.ASSET_CLAIM_FEES = 15
        self.PROPOSAL_CREATE = 16
        self.PROPOSAL_UPDATE = 17
        self.PROPOSAL_DELETE = 18
        self.COMMITTEE_MEMBER_CREATE = 19
        self.COMMITTEE_MEMBER_UPDATE = 20
        self.COMMITTEE_MEMBER_UPDATE_GLOBAL_PARAMETERS = 21
        self.COMMITTEE_MEMBER_ACTIVATE = 22
        self.COMMITTEE_MEMBER_DEACTIVATE = 23
        self.COMMITTEE_FROZEN_BALANCE_DEPOSIT = 24
        self.COMMITTEE_FROZEN_BALANCE_WITHDRAW = 25
        self.VESTING_BALANCE_CREATE = 26
        self.VESTING_BALANCE_WITHDRAW = 27
        self.BALANCE_CLAIM = 28
        self.BALANCE_FREEZE = 29
        self.BALANCE_UNFREEZE = 30
        self.REQUEST_BALANCE_UNFREEZE = 31
        self.CONTRACT_CREATE = 32
        self.CONTRACT_CALL = 33
        self.CONTRACT_INTERNAL_CREATE = 34
        self.CONTRACT_INTERNAL_CALL = 35
        self.CONTRACT_SELFDESTRUCT = 36
        self.CONTRACT_UPDATE = 37
        self.CONTRACT_FUND_POOL = 38
        self.CONTRACT_WHITELIST = 39
        self.SIDECHAIN_ETH_CREATE_ADDRESS = 40
        self.SIDECHAIN_ETH_APPROVE_ADDRESS = 41
        self.SIDECHAIN_ETH_DEPOSIT = 42
        self.SIDECHAIN_ETH_SEND_DEPOSIT = 43
        self.SIDECHAIN_ETH_WITHDRAW = 44
        self.SIDECHAIN_ETH_SEND_WITHDRAW = 45
        self.SIDECHAIN_ETH_APPROVE_WITHDRAW = 46
        self.SIDECHAIN_ETH_UPDATE_CONTRACT_ADDRESS = 47
        self.SIDECHAIN_ISSUE = 48
        self.SIDECHAIN_BURN = 49
        self.SIDECHAIN_ERC20_REGISTER_TOKEN = 50
        self.SIDECHAIN_ERC20_DEPOSIT_TOKEN = 51
        self.SIDECHAIN_ERC20_SEND_DEPOSIT_TOKEN = 52
        self.SIDECHAIN_ERC20_WITHDRAW_TOKEN = 53
        self.SIDECHAIN_ERC20_SEND_WITHDRAW_TOKEN = 54
        self.SIDECHAIN_ERC20_APPROVE_TOKEN_WITHDRAW = 55
        self.SIDECHAIN_ERC20_ISSUE = 56
        self.SIDECHAIN_ERC20_BURN = 57
        self.SIDECHAIN_BTC_CREATE_ADDRESS = 58
        self.SIDECHAIN_BTC_CREATE_INTERMEDIATE_DEPOSIT = 59
        self.SIDECHAIN_BTC_INTERMEDIATE_DEPOSIT = 60
        self.SIDECHAIN_BTC_DEPOSIT = 61
        self.SIDECHAIN_BTC_WITHDRAW = 62
        self.SIDECHAIN_BTC_AGGREGATE = 63
        self.SIDECHAIN_BTC_APPROVE_AGGREGATE = 64
        self.SIDECHAIN_STAKE_ETH_UPDATE = 65
        self.SIDECHAIN_STAKE_BTC_CREATE_SCRIPT = 66
        self.SIDECHAIN_STAKE_BTC_UPDATE = 67
        self.BLOCK_REWARD = 68
        self.EVM_ADDRESS_REGISTER = 69
        self.DID_CREATE = 70
        self.DID_UPDATE = 71
        self.DID_DELETE = 72
