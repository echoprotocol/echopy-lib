# -*- coding: utf-8 -*-
from collections import OrderedDict

from .operationids import operations
from .objects import EchoObject, isArgsThisClass
from .types import (
    Uint32,
    Uint64,
)
from .types import StaticVariant


class FeeTypes(StaticVariant):
    def __init__(self, o):
        class NoFee(EchoObject):
            def __init__(self, kwargs):
                    super().__init__(OrderedDict([]))

        class DefaultFee(EchoObject):
            def __init__(self, *args, **kwargs):
                    if isArgsThisClass(self, args):
                        self.data = args[0].data
                    else:
                        if len(args) == 1 and len(kwargs) == 0:
                            kwargs = args[0]
                        super().__init__(
                            OrderedDict(
                                [
                                    ("fee", Uint64(kwargs["fee"])),
                                ]
                            )
                        )

        class WithPricePerKB(EchoObject):
            def __init__(self, *args, **kwargs):
                    if isArgsThisClass(self, args):
                        self.data = args[0].data
                    else:
                        if len(args) == 1 and len(kwargs) == 0:
                            kwargs = args[0]
                        super().__init__(
                            OrderedDict(
                                [
                                    ("fee", Uint64(kwargs["fee"])),
                                    ("price_per_kbyte", Uint32(kwargs["price_per_kbyte"])),
                                ]
                            )
                        )

        class AccountCreate(EchoObject):
            def __init__(self, *args, **kwargs):
                    if isArgsThisClass(self, args):
                        self.data = args[0].data
                    else:
                        if len(args) == 1 and len(kwargs) == 0:
                            kwargs = args[0]
                        super().__init__(
                            OrderedDict(
                                [
                                    ("basic_fee", Uint64(kwargs["basic_fee"])),
                                    ("premium_fee", Uint64(kwargs["premium_fee"])),
                                    ("price_per_kbyte", Uint32(kwargs["price_per_kbyte"])),
                                ]
                            )
                        )

        class AccountUpgrade(EchoObject):
            def __init__(self, *args, **kwargs):
                    if isArgsThisClass(self, args):
                        self.data = args[0].data
                    else:
                        if len(args) == 1 and len(kwargs) == 0:
                            kwargs = args[0]
                        super().__init__(
                            OrderedDict(
                                [
                                    ("membership_annual_fee", Uint64(kwargs["membership_annual_fee"])),
                                    ("membership_lifetime_fee", Uint64(kwargs["membership_lifetime_fee"])),
                                ]
                            )
                        )

        class AssetCreate(EchoObject):
            def __init__(self, *args, **kwargs):
                    if isArgsThisClass(self, args):
                        self.data = args[0].data
                    else:
                        if len(args) == 1 and len(kwargs) == 0:
                            kwargs = args[0]
                        super().__init__(
                            OrderedDict(
                                [
                                    ("symbol3", Uint64(kwargs["symbol3"])),
                                    ("symbol4", Uint64(kwargs["symbol4"])),
                                    ("long_symbol", Uint64(kwargs["long_symbol"])),
                                    ("price_per_kbyte", Uint32(kwargs["price_per_kbyte"])),
                                ]
                            )
                        )

        class Erc20RegisterToken(EchoObject):
            def __init__(self, *args, **kwargs):
                    if isArgsThisClass(self, args):
                        self.data = args[0].data
                    else:
                        if len(args) == 1 and len(kwargs) == 0:
                            kwargs = args[0]
                        super().__init__(
                            OrderedDict(
                                [
                                    ("fee", Uint64(kwargs["fee"])),
                                    ("pool_fee", Uint64(kwargs["pool_fee"])),
                                ]
                            )
                        )

        ops = {
            operations["transfer"]: DefaultFee,
            operations["transfer_to_address"]: DefaultFee,
            operations["override_transfer"]: DefaultFee,
            operations["account_create"]: AccountCreate,
            operations["account_update"]: WithPricePerKB,
            operations["account_whitelist"]: DefaultFee,
            operations["account_address_create"]: WithPricePerKB,
            operations["asset_create"]: AssetCreate,
            operations["asset_update"]: WithPricePerKB,
            operations["asset_update_bitasset"]: DefaultFee,
            operations["asset_update_feed_producers"]: DefaultFee,
            operations["asset_issue"]: DefaultFee,
            operations["asset_reserve"]: DefaultFee,
            operations["asset_fund_fee_pool"]: DefaultFee,
            operations["asset_publish_feed"]: DefaultFee,
            operations["asset_claim_fees"]: DefaultFee,
            operations["proposal_create"]: WithPricePerKB,
            operations["proposal_update"]: WithPricePerKB,
            operations["proposal_delete"]: DefaultFee,
            operations["committee_member_create"]: DefaultFee,
            operations["committee_member_update"]: DefaultFee,
            operations["committee_member_update_global_parameters"]: DefaultFee,
            operations["committee_member_activate"]: DefaultFee,
            operations["committee_member_deactivate"]: DefaultFee,
            operations["committee_frozen_balance_deposit"]: DefaultFee,
            operations["committee_frozen_balance_withdraw"]: DefaultFee,
            operations["vesting_balance_create"]: DefaultFee,
            operations["vesting_balance_withdraw"]: DefaultFee,
            operations["balance_claim"]: NoFee,
            operations["balance_freeze"]: DefaultFee,
            operations["balance_unfreeze"]: NoFee,
            operations["contract_create"]: DefaultFee,
            operations["contract_call"]: DefaultFee,
            operations["contract_internal_create"]: NoFee,
            operations["contract_internal_call"]: NoFee,
            operations["contract_selfdestruct"]: NoFee,
            operations["contract_update"]: DefaultFee,
            operations["contract_fund_pool"]: DefaultFee,
            operations["contract_whitelist"]: DefaultFee,
            operations["sidechain_eth_create_address"]: DefaultFee,
            operations["sidechain_eth_approve_address"]: DefaultFee,
            operations["sidechain_eth_deposit"]: DefaultFee,
            operations["sidechain_eth_send_deposit"]: DefaultFee,
            operations["sidechain_eth_withdraw"]: DefaultFee,
            operations["sidechain_eth_send_withdraw"]: DefaultFee,
            operations["sidechain_eth_approve_withdraw"]: DefaultFee,
            operations["sidechain_eth_update_contract_address"]: DefaultFee,
            operations["sidechain_issue"]: DefaultFee,
            operations["sidechain_burn"]: DefaultFee,
            operations["sidechain_erc20_register_token"]: Erc20RegisterToken,
            operations["sidechain_erc20_deposit_token"]: DefaultFee,
            operations["sidechain_erc20_send_deposit_token"]: DefaultFee,
            operations["sidechain_erc20_withdraw_token"]: DefaultFee,
            operations["sidechain_erc20_send_withdraw_token"]: DefaultFee,
            operations["sidechain_erc20_approve_token_withdraw"]: DefaultFee,
            operations["sidechain_erc20_issue"]: DefaultFee,
            operations["sidechain_erc20_burn"]: DefaultFee,
            operations["sidechain_btc_create_address"]: DefaultFee,
            operations["sidechain_btc_create_intermediate_deposit"]: DefaultFee,
            operations["sidechain_btc_intermediate_deposit"]: DefaultFee,
            operations["sidechain_btc_deposit"]: DefaultFee,
            operations["sidechain_btc_withdraw"]: DefaultFee,
            operations["sidechain_btc_aggregate"]: DefaultFee,
            operations["sidechain_btc_approve_aggregate"]: DefaultFee,
            operations["block_reward"]: NoFee
        }

        ops_key, params = o
        super().__init__(ops_key, ops[ops_key](params))
