# -*- coding: utf-8 -*-
from collections import OrderedDict

from .operationids import operations
from .objects import EchoObject, isArgsThisClass
from .types import (
    Uint32,
    Uint64,
)
from .types import Static_variant


class FeeTypes(Static_variant):
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

        class WithPricePerOutput(EchoObject):
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
                                    ("price_per_output", Uint32(kwargs["price_per_output"])),
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
        ops = {
            operations["transfer"]: WithPricePerKB,
            operations["limit_order_create"]: DefaultFee,
            operations["limit_order_cancel"]: DefaultFee,
            operations["call_order_update"]: DefaultFee,
            operations["fill_order"]: NoFee,
            operations["account_create"]: AccountCreate,
            operations["account_update"]: WithPricePerKB,
            operations["account_whitelist"]: DefaultFee,
            operations["account_upgrade"]: AccountUpgrade,
            operations["account_transfer"]: DefaultFee,
            operations["asset_create"]: AssetCreate,
            operations["asset_update"]: WithPricePerKB,
            operations["asset_update_bitasset"]: DefaultFee,
            operations["asset_update_feed_producers"]: DefaultFee,
            operations["asset_issue"]: WithPricePerKB,
            operations["asset_reserve"]: DefaultFee,
            operations["asset_fund_fee_pool"]: DefaultFee,
            operations["asset_settle"]: DefaultFee,
            operations["asset_global_settle"]: DefaultFee,
            operations["asset_publish_feed"]: DefaultFee,
            operations["witness_create"]: DefaultFee,
            operations["witness_update"]: DefaultFee,
            operations["proposal_create"]: WithPricePerKB,
            operations["proposal_update"]: WithPricePerKB,
            operations["proposal_delete"]: DefaultFee,
            operations["withdraw_permission_create"]: DefaultFee,
            operations["withdraw_permission_update"]: DefaultFee,
            operations["withdraw_permission_claim"]: WithPricePerKB,
            operations["withdraw_permission_delete"]: DefaultFee,
            operations["committee_member_create"]: DefaultFee,
            operations["committee_member_update"]: DefaultFee,
            operations["committee_member_update_global_parameters"]: DefaultFee,
            operations["vesting_balance_create"]: DefaultFee,
            operations["vesting_balance_withdraw"]: DefaultFee,
            operations["worker_create"]: DefaultFee,
            operations["custom"]: WithPricePerKB,
            operations["assert"]: DefaultFee,
            operations["balance_claim"]: NoFee,
            operations["override_transfer"]: WithPricePerKB,
            operations["transfer_to_blind"]: WithPricePerOutput,
            operations["blind_transfer"]: WithPricePerOutput,
            operations["transfer_from_blind"]: DefaultFee,
            operations["asset_settle_cancel"]: NoFee,
            operations["asset_claim_fees"]: DefaultFee,
            operations["fba_distribute"]: NoFee,
            operations["bid_collateral"]: DefaultFee,
            operations["execute_bid"]: NoFee,
            operations["create_contract"]: DefaultFee,
            operations["call_contract"]: DefaultFee,
            operations["contract_transfer"]: DefaultFee
        }

        ops_key, params = o
        super().__init__(ops[ops_key](params), ops_key)
