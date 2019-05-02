#: chain_types
class ChainTypes:
    def __init__(self):
        self.reserved_spaces = {
            'RELATIVE_PROTOCOL_IDS': 0,
            'PROTOCOL_IDS': 1,
            'IMPLEMENTATION_IDS': 2,
        }

        self.implementation_object_type = {
            'GLOBAL_PROPERTY': 0,
            'DYNAMIC_GLOBAL_PROPERTY': 1,
            'RESERVED0': 2,
            'ASSET_DYNAMIC_DATA': 3,
            'ASSET_BITASSET_DATA': 4,
            'ACCOUNT_BALANCE': 5,
            'ACCOUNT_STATISTICS': 6,
            'TRANSACTION': 7,
            'BLOCK_SUMMARY': 8,
            'ACCOUNT_TRANSACTION_HISTORY': 9,
            'CHAIN_PROPERTY': 10,
            'BUDGET_RECORD': 11,
            'SPECIAL_AUTHORITY': 12,
            'BUYBACK': 13,
            'COLLATERAL_BID': 14,
            'CONTRACT_BALANCE': 15,
            'CONTRACT_HISTORY': 16,
            'CONTRACT_STATISTICS': 17,
        }

        self.vote_type = {
            'COMMITTEE': 0,
        }
