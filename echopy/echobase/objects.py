# -*- coding: utf-8 -*-
import json

from collections import OrderedDict
from .types import (
    Uint8,
    Uint16,
    Uint32,
    Uint64,
    Int64,
    String,
    Bytes,
    Array,
    PointInTime,
    Bool,
    Set,
    Optional,
    StaticVariant,
    Map,
    VoteId,
    JsonObj,
)
from .types import ObjectId as ObjectIdParent
from .objecttypes import object_type
from .account import PublicKey


default_prefix = "ECHO"


class EchoObject(OrderedDict):
    """ This class is used for any JSON reflected object in ECHO.
    """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (dict, OrderedDict)):
            if hasattr(self, "detail"):
                super().__init__(self.detail(**args[0]))
            else:
                OrderedDict.__init__(self, args[0])
            return

        elif kwargs and hasattr(self, "detail"):
            super().__init__(self.detail(*args, **kwargs))

    def __bytes__(self):
        if len(self) is 0:
            return bytes()
        b = b""
        for name in self.keys():
            value = self[name]
            if isinstance(value, str):
                b += bytes(value, "utf-8")
            else:
                b += bytes(value)
        return b

    def __json__(self):
        if len(self) is 0:
            return {}

        d = OrderedDict([])
        for k in self.keys():
            value = self[k]
            name = k
            if isinstance(value, Optional) and value.isempty():
                continue

            if isinstance(value, String):
                d.update({name: str(value)})
            else:
                try:
                    d.update({name: JsonObj(value)})
                except Exception:
                    d.update({name: value.__str__()})
        return d

    def __str__(self):
        return json.dumps(self.__json__())

    def add_fee(self, ordered_dict, kwargs):
        if 'fee' in kwargs:
            ordered_dict.update({"fee": Asset(kwargs["fee"])})
            ordered_dict.move_to_end("fee", last=False)

    @property
    def data(self):
        return self

    @data.setter
    def data(self, data):
        self.update(data)

    toJson = __json__
    json = __json__


class ObjectId(ObjectIdParent):
    """ Need to overwrite a few attributes to load proper object_types from
        ECHO
    """

    object_types = object_type


class Memo(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            if "message" in kwargs and kwargs["message"]:
                super().__init__(
                    OrderedDict(
                        [
                            ("from", PublicKey(kwargs["from"], prefix='ECHO')),
                            ("to", PublicKey(kwargs["to"], prefix='ECHO')),
                            ("nonce", Uint64(int(kwargs["nonce"]))),
                            ("message", Bytes(kwargs["message"])),
                        ]
                    )
                )
            else:
                super().__init__(None)


class Price(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [("base", Asset(kwargs["base"])), ("quote", Asset(kwargs["quote"]))]
                )
            )


class PriceFeed(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("settlement_price", Price(kwargs["settlement_price"])),
                        (
                            "maintenance_collateral_ratio",
                            Uint16(kwargs["maintenance_collateral_ratio"]),
                        ),
                        (
                            "maximum_short_squeeze_ratio",
                            Uint16(kwargs["maximum_short_squeeze_ratio"]),
                        ),
                        ("core_exchange_rate", Price(kwargs["core_exchange_rate"])),
                    ]
                )
            )


class Permission(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]

            account_auths = Map(
                [
                    [ObjectId(e[0], "account"), Uint16(e[1])]
                    for e in kwargs["account_auths"]
                ]
            )
            key_auths = Map(
                [
                    [PublicKey(e[0]), Uint16(e[1])]
                    for e in kwargs["key_auths"]
                ]
            )
            super().__init__(
                OrderedDict(
                    [
                        ("weight_threshold", Uint32(kwargs["weight_threshold"])),
                        ("account_auths", account_auths),
                        ("key_auths", key_auths),
                    ]
                )
            )


class AccountOptions(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            kwargs["votes"] = list(set(kwargs["votes"]))
            kwargs["votes"] = sorted(
                kwargs["votes"], key=lambda x: float(x.split(":")[1])
            )
            super().__init__(
                OrderedDict(
                    [
                        ("voting_account", ObjectId(kwargs["voting_account"], "account")),
                        ("delegating_account", ObjectId(kwargs["delegating_account"], "account")),
                        ("num_committee", Uint16(kwargs["num_committee"])),
                        ("votes", Set([VoteId(o) for o in kwargs["votes"]])),
                        ("extensions", Set([])),
                    ]
                )
            )


class AssetOptions(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("max_supply", Int64(kwargs["max_supply"])),
                        ("market_fee_percent", Uint16(kwargs["market_fee_percent"])),
                        ("max_market_fee", Int64(kwargs["max_market_fee"])),
                        ("issuer_permissions", Uint16(kwargs["issuer_permissions"])),
                        ("flags", Uint16(kwargs["flags"])),
                        ("core_exchange_rate", Price(kwargs["core_exchange_rate"])),
                        (
                            "whitelist_authorities",
                            Array(
                                [
                                    ObjectId(x, "account")
                                    for x in kwargs["whitelist_authorities"]
                                ]
                            ),
                        ),
                        (
                            "blacklist_authorities",
                            Array(
                                [
                                    ObjectId(x, "account")
                                    for x in kwargs["blacklist_authorities"]
                                ]
                            ),
                        ),
                        (
                            "whitelist_markets",
                            Array(
                                [
                                    ObjectId(x, "asset")
                                    for x in kwargs["whitelist_markets"]
                                ]
                            ),
                        ),
                        (
                            "blacklist_markets",
                            Array(
                                [
                                    ObjectId(x, "asset")
                                    for x in kwargs["blacklist_markets"]
                                ]
                            ),
                        ),
                        ("description", String(kwargs["description"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class BitAssetOptions(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("feed_lifetime_sec", Uint32(kwargs["feed_lifetime_sec"])),
                        ("minimum_feeds", Uint8(kwargs["minimum_feeds"])),
                        (
                            "force_settlement_delay_sec",
                            Uint32(kwargs["force_settlement_delay_sec"]),
                        ),
                        (
                            "force_settlement_offset_percent",
                            Uint16(kwargs["force_settlement_offset_percent"]),
                        ),
                        (
                            "maximum_force_settlement_volume",
                            Uint16(kwargs["maximum_force_settlement_volume"]),
                        ),
                        (
                            "short_backing_asset",
                            ObjectId(kwargs["short_backing_asset"], "asset"),
                        ),
                        ("extensions", Set([])),
                    ]
                )
            )


def isArgsThisClass(self, args):
    return len(args) == 1 and type(args[0]).__name__ == type(self).__name__


class Asset(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            asset = OrderedDict()
            if 'amount' in kwargs:
                asset.update({'amount': Int64(kwargs['amount'])})
            if 'asset_id' in kwargs:
                asset.update({'asset_id': ObjectId(kwargs['asset_id'], 'asset')})
            super().__init__(asset)


class VestingPolicyInitializer(StaticVariant):
    def __init__(self, o):
        class LinearVestingPolicyInitializer(EchoObject):
            def __init__(self, *args, **kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(
                        OrderedDict(
                            [
                                ("begin_timestamp", PointInTime(kwargs["begin_timestamp"])),
                                ("vesting_cliff_seconds", Uint32(kwargs["vesting_cliff_seconds"])),
                                ("vesting_duration_seconds", Uint32(kwargs["vesting_duration_seconds"])),
                            ]
                        )
                    )

        class CddVestingPolicyInitializer(EchoObject):
            def __init__(self, *args, **kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(
                        OrderedDict(
                            [
                                ("start_claim", PointInTime(kwargs["start_claim"])),
                                ("vesting_seconds", Uint32(kwargs["vesting_seconds"])),
                            ]
                        )
                    )

        _id = o[0]
        if _id == 0:
            data = LinearVestingPolicyInitializer(o[1])
        elif _id == 1:
            data = CddVestingPolicyInitializer(o[1])
        else:
            raise Exception("Unknown vesting_policy_initializer")
        super().__init__(data, _id)


class WorkerInitializer(StaticVariant):
    def __init__(self, o):
        class BurnWorkerInitializer(EchoObject):
            def __init__(self, kwargs):
                super().__init__(OrderedDict([]))

        class RefundWorkerInitializer(EchoObject):
            def __init__(self, kwargs):
                super().__init__(OrderedDict([]))

        class VestingBalanceWorkerInitializer(EchoObject):
            def __init__(self, *args, **kwargs):
                if isArgsThisClass(self, args):
                    self.data = args[0].data
                else:
                    if len(args) == 1 and len(kwargs) == 0:
                        kwargs = args[0]
                    super().__init__(
                        OrderedDict(
                            [
                                (
                                    "pay_vesting_period_days",
                                    Uint16(kwargs["pay_vesting_period_days"]),
                                )
                            ]
                        )
                    )

        _id = o[0]
        if _id == 0:
            data = RefundWorkerInitializer(o[1])
        elif _id == 1:
            data = VestingBalanceWorkerInitializer(o[1])
        elif _id == 2:
            data = BurnWorkerInitializer(o[1])
        else:
            raise Exception("Unknown Worker_initializer")
        super().__init__(data, id)


class FeeSchedule(EchoObject):
    def __init__(self, *args, **kwargs):
        from .feetypes import Fee_types
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("parameters", Set([Fee_types(param) for param in kwargs["parameters"]])),
                        ("scale", Uint32(kwargs["scale"]))
                    ]
                )
            )

class EchorandConfig(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("time_net_1mb", Uint32(kwargs["time_net_1mb"])),
                        ("time_net_256b", Uint32(kwargs["time_net_256b"])),
                        ("creator_count", Uint32(kwargs["creator_count"])),
                        ("verifier_count", Uint32(kwargs["verifier_count"])),
                        ("ok_treshold", Uint32(kwargs["ok_treshold"])),
                        ("max_bba_steps", Uint32(kwargs["max_bba_steps"])),
                        ("gc1_delay", Uint32(kwargs["gc1_delay"]))
                    ]
                )
            )


class SidechainConfig(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("eth_contarct_address", String(kwargs["eth_contarct_address"])),
                        ("eth_committee_update_method", EthMethod(kwargs["eth_committee_update_method"])),
                        ("eth_gen_address_method", EthMethod(kwargs["eth_gen_address_method"])),
                        ("eth_withdraw_method", EthMethod(kwargs["eth_withdraw_method"])),
                        ("eth_update_addr_method", EthMethod(kwargs["eth_update_addr_method"])),
                        ("eth_committee_updated_topic", String(kwargs["eth_committee_updated_topic"])),
                        ("eth_gen_address_topic", String(kwargs["eth_gen_address_topic"])),
                        ("eth_deposit_topic", String(kwargs["eth_deposit_topic"])),
                        ("eth_withdraw_topic", String(kwargs["eth_withdraw_topic"])),
                        ("ETH_asset_id", ObjectId(kwargs["ETH_asset_id", "asset"]))
                    ]
                )
            )


class EthMethod(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("method", String(kwargs["method"])),
                        ("gas", Uint64(kwargs["gas"]))
                    ]
                )
            )



class GasPrice(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("price", Uint64(kwargs["price"])),
                        ("gas_amount", Uint64(kwargs["gas_amount"]))
                    ]
                )
            )


class ChainParameters(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("current_fees", FeeSchedule(kwargs["current_fees"])),
                        ("block_interval", Uint8(kwargs["block_interval"])),
                        ("maintenance_interval", Uint32(kwargs["maintenance_interval"])),
                        ("maintenance_skip_slots", Uint8(kwargs["maintenance_skip_slots"])),
                        ("committee_proposal_review_period", Uint32(kwargs["committee_proposal_review_period"])),
                        ("maximum_transaction_size", Uint32(kwargs["maximum_transaction_size"])),
                        ("maximum_block_size", Uint32(kwargs["maximum_block_size"])),
                        ("maximum_time_until_expiration", Uint32(kwargs["maximum_time_until_expiration"])),
                        ("maximum_proposal_lifetime", Uint32(kwargs["maximum_proposal_lifetime"])),
                        ("maximum_asset_whitelist_authorities", Uint8(
                            kwargs["maximum_asset_whitelist_authorities"]
                        )),
                        ("maximum_asset_feed_publishers", Uint8(kwargs["maximum_asset_feed_publishers"])),
                        ("maximum_committee_count", Uint16(kwargs["maximum_committee_count"])),
                        ("maximum_authority_membership", Uint16(kwargs["maximum_authority_membership"])),
                        ("reserve_percent_of_fee", Uint16(kwargs["reserve_percent_of_fee"])),
                        ("network_percent_of_fee", Uint16(kwargs["network_percent_of_fee"])),
                        ("lifetime_referrer_percent_of_fee", Uint16(kwargs["lifetime_referrer_percent_of_fee"])),
                        ("cashback_vesting_period_seconds", Uint32(kwargs["cashback_vesting_period_seconds"])),
                        ("cashback_vesting_threshold", Int64(kwargs["cashback_vesting_threshold"])),
                        ("count_non_member_votes", Bool(kwargs["count_non_member_votes"])),
                        ("allow_non_member_whitelists", Bool(kwargs["allow_non_member_whitelists"])),
                        ("max_predicate_opcode", Uint16(kwargs["max_predicate_opcode"])),
                        ("fee_liquidation_threshold", Int64(kwargs["fee_liquidation_threshold"])),
                        ("accounts_per_fee_scale", Uint16(kwargs["accounts_per_fee_scale"])),
                        ("account_fee_scale_bitshifts", Uint8(kwargs["account_fee_scale_bitshifts"])),
                        ("max_authority_depth", Uint8(kwargs["max_authority_depth"])),
                        ("echorand_config", EchorandConfig(kwargs["echorand_config"])),
                        ("sidechain_config", SidechainConfig(kwargs["sidechain_config"])),
                        ("gas_price", GasPrice(kwargs["gas_price"])),
                        ("extensions", Set([])),
                    ]
                )
            )
