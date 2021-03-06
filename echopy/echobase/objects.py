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
    Sha256
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


class OpWrapper(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(

                OrderedDict(
                    [
                        ("op", StaticVariant(kwargs["op"][0], kwargs["op"][1])),
                    ]
                )
            )


class ObjectId(ObjectIdParent):
    """ Need to overwrite a few attributes to load proper object_types from
        ECHO
    """

    object_types = object_type


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

            kwargs["key_auths"] = sorted(
                kwargs["key_auths"],
                key=lambda x: PublicKey(x[0], prefix='ECHO'),
                reverse=False,
            )

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
            super().__init__(
                OrderedDict(
                    [
                        ("delegating_account", ObjectId(kwargs["delegating_account"], "account")),
                        ("delegate_share", Uint16(kwargs["delegate_share"])),
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
                        ("issuer_permissions", Uint16(kwargs["issuer_permissions"])),
                        ("flags", Uint16(kwargs["flags"])),
                        ("core_exchange_rate", Price(kwargs["core_exchange_rate"])),
                        (
                            "whitelist_authorities",
                            Set(
                                [
                                    ObjectId(x, "account")
                                    for x in kwargs["whitelist_authorities"]
                                ]
                            ),
                        ),
                        (
                            "blacklist_authorities",
                            Set(
                                [
                                    ObjectId(x, "account")
                                    for x in kwargs["blacklist_authorities"]
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
        super().__init__(_id, data)


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
        super().__init__(_id, data)


class FeeSchedule(EchoObject):
    def __init__(self, *args, **kwargs):
        from echopy.echobase import feetypes
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("parameters", Set([feetypes.FeeTypes(param) for param in kwargs["parameters"]])),
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
                        ("_time_generate", Uint32(kwargs["_time_generate"])),
                        ("_time_net_1mb", Uint32(kwargs["_time_net_1mb"])),
                        ("_time_net_256b", Uint32(kwargs["_time_net_256b"])),
                        ("_creator_count", Uint32(kwargs["_creator_count"])),
                        ("_verifier_count", Uint32(kwargs["_verifier_count"])),
                        ("_ok_threshold", Uint32(kwargs["_ok_threshold"])),
                        ("_max_bba_steps", Uint32(kwargs["_max_bba_steps"])),
                        ("_gc1_delay", Uint32(kwargs["_gc1_delay"])),
                        ("_round_attempts", Uint32(kwargs["_round_attempts"])),
                    ]
                )
            )


class EthAddress(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("create_eth_address", Int64(kwargs["create_eth_address"]))
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
                        ("eth_contract_address", Bytes(kwargs["eth_contract_address"])),
                        ("eth_committee_update_method", EthMethod(kwargs["eth_committee_update_method"])),
                        ("eth_gen_address_method", EthMethod(kwargs["eth_gen_address_method"])),
                        ("eth_withdraw_method", EthMethod(kwargs["eth_withdraw_method"])),
                        ("eth_update_addr_method", EthMethod(kwargs["eth_update_addr_method"])),
                        ("eth_update_contract_address", EthMethod(kwargs["eth_update_contract_address"])),
                        ("eth_withdraw_token_method", EthMethod(kwargs["eth_withdraw_token_method"])),
                        ("eth_collect_tokens_method", EthMethod(kwargs["eth_collect_tokens_method"])),
                        ("eth_committee_updated_topic", Bytes(kwargs["eth_committee_updated_topic"], 32)),
                        ("eth_gen_address_topic", Bytes(kwargs["eth_gen_address_topic"], 32)),
                        ("eth_deposit_topic", Bytes(kwargs["eth_deposit_topic"], 32)),
                        ("eth_withdraw_topic", Bytes(kwargs["eth_withdraw_topic"], 32)),
                        ("erc20_deposit_topic", Bytes(kwargs["erc20_deposit_topic"], 32)),
                        ("erc20_withdraw_topic", Bytes(kwargs["erc20_withdraw_topic"], 32)),
                        ("ETH_asset_id", ObjectId(kwargs["ETH_asset_id"], "asset")),
                        ("BTC_asset_id", ObjectId(kwargs["BTC_asset_id"], "asset")),
                        ("fines", EthAddress(kwargs["fines"])),
                        ("gas_price", Uint64(kwargs["gas_price"])),
                        ("satoshis_per_byte", Uint32(kwargs["satoshis_per_byte"])),
                        ("coefficient_waiting_blocks", Uint32(kwargs["coefficient_waiting_blocks"])),
                        ("btc_deposit_withdrawal_min", Uint64(kwargs["btc_deposit_withdrawal_min"])),
                        ("btc_deposit_withdrawal_fee", Uint64(kwargs["btc_deposit_withdrawal_fee"]))
                    ]
                )
            )


class Erc20Config(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("contract_code", String(kwargs["contract_code"])),
                        ("create_token_fee", Uint64(kwargs["create_token_fee"])),
                        ("transfer_topic", Bytes(kwargs["transfer_topic"], 32)),
                        ("check_balance_method", EthMethod(kwargs["check_balance_method"])),
                        ("burn_method", EthMethod(kwargs["burn_method"])),
                        ("issue_method", EthMethod(kwargs["issue_method"])),
                    ]
                )
            )

class StakeConfig(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("contract_address", Bytes(kwargs["contract_address"])),
                        ("balance_updated_topic", Bytes(kwargs["balance_updated_topic"])),
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


class EconomyConfig(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("blocks_in_interval", Uint64(kwargs["blocks_in_interval"])),
                        ("maintenances_in_interval", Uint8(kwargs["maintenances_in_interval"])),
                        ("block_emission_amount", Uint64(kwargs["block_emission_amount"])),
                        ("block_producer_reward_ratio", Uint16(kwargs["block_producer_reward_ratio"])),
                        ("pool_divider", Uint16(kwargs["pool_divider"])),
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
                        ("maintenance_interval", Uint32(kwargs["maintenance_interval"])),
                        ("maintenance_duration_seconds", Uint8(kwargs["maintenance_duration_seconds"])),
                        ("balance_unfreezing_time", Uint32(kwargs["balance_unfreezing_time"])),
                        ("committee_proposal_review_period", Uint32(kwargs["committee_proposal_review_period"])),
                        ("maximum_transaction_size", Uint32(kwargs["maximum_transaction_size"])),
                        ("maximum_block_size", Uint32(kwargs["maximum_block_size"])),
                        ("maximum_time_until_expiration", Uint32(kwargs["maximum_time_until_expiration"])),
                        ("maximum_proposal_lifetime", Uint32(kwargs["maximum_proposal_lifetime"])),
                        ("maximum_asset_whitelist_authorities", Uint8(
                            kwargs["maximum_asset_whitelist_authorities"]
                        )),
                        ("maximum_asset_feed_publishers", Uint8(kwargs["maximum_asset_feed_publishers"])),
                        ("maximum_authority_membership", Uint16(kwargs["maximum_authority_membership"])),
                        ("max_authority_depth", Uint8(kwargs["max_authority_depth"])),

                        ("committee_frozen_balance_to_activate",
                            Uint64(kwargs["committee_frozen_balance_to_activate"])),
                        ("committee_maintenance_intervals_to_deposit",
                            Uint64(kwargs["committee_maintenance_intervals_to_deposit"])),
                        ("committee_balance_unfreeze_duration_seconds",
                            Uint32(kwargs["committee_balance_unfreeze_duration_seconds"])),

                        ("x86_64_maximum_contract_size", Uint64(kwargs["x86_64_maximum_contract_size"])),

                        ("frozen_balances_multipliers", Map(
                            [[Uint16(e[0]), Uint32(e[1])] for e in kwargs["frozen_balances_multipliers"]]
                        )),

                        ("echorand_config", EchorandConfig(kwargs["echorand_config"])),
                        ("sidechain_config", SidechainConfig(kwargs["sidechain_config"])),
                        ("erc20_config", Erc20Config(kwargs["erc20_config"])),
                        ("stake_sidechain_config", StakeConfig(kwargs["stake_sidechain_config"])),

                        ("gas_price", GasPrice(kwargs["gas_price"])),
                        ("consensus_assets", Set([ObjectId(i, "asset") for i in kwargs["consensus_assets"]])),
                        ("valid_fee_asset", Set([ObjectId(i, "asset") for i in kwargs["valid_fee_asset"]])),
                        ("economy_config", EconomyConfig(kwargs["economy_config"])),
                        ("extensions", Set([])),
                    ]
                )
            )


class BtcTransactionDetails(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("block_number", Uint64(kwargs["block_number"])),
                        ("tx_id", String(kwargs["tx_id"])),
                        ("index", Uint32(kwargs["index"])),
                        ("amount", Uint64(kwargs["amount"])),
                    ]
                )
            )


class P2shP2wsh(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("address", String(kwargs["address"])),
                    ]
                )
            )


class BtcTxInfo(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("block_number", Uint64(kwargs["block_number"])),
                        ("out", BtcTxInfoOut(kwargs['out']))
                    ]
                )
            )


class BtcTxInfoOut(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("tx_id", Sha256(kwargs["tx_id"])),
                        ("index", Uint32(kwargs["index"])),
                        ("amount", Uint64(kwargs["amount"]))
                    ]
                )
            )
