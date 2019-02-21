# -*- coding: utf-8 -*-
import json

from collections import OrderedDict
from .types import (
    Uint8,
    Uint16,
    Uint32,
    Uint64,
    Varint32,
    Int64,
    String,
    Bytes,
    Void,
    Array,
    PointInTime,
    Signature,
    Bool,
    Set,
    FixedArray,
    Optional,
    StaticVariant,
    Map,
    Id,
    VoteId,
    JsonObj,
)
from .types import ObjectId as ObjectIdParent
from .chains import known_chains
from .objecttypes import object_type
from .account import PublicKey
from .chains import default_prefix
from .operationids import operations


class Operation(list):
    """ The superclass for an operation. This class i used to instanciate an
        operation, identify the operationid/name and serialize the operation
        into bytes.
    """

    module = "echobase.operations"
    fromlist = ["operations"]
    operations = operations

    def __init__(self, op, **kwargs):
        list.__init__(self, [0, EchoObject()])

        # Are we dealing with an actual operation as list of opid and payload?
        if isinstance(op, list) and len(op) == 2:
            self._setidanename(op[0])
            self.set(**op[1])

        # Here, we allow to only load the Operation as Template without data
        elif isinstance(op, str) or isinstance(op, int):
            self._setidanename(op)
            if kwargs:
                self.set(**kwargs)

        elif isinstance(op, EchoObject):
            self._loadEchoObject(op)

        else:
            raise ValueError("Unknown format for Operation({})".format(type(op)))

    @property
    def id(self):
        return self[0]

    @id.setter
    def id(self, value):
        assert isinstance(value, int)
        self[0] = value

    @property
    def operation(self):
        return self[1]

    @operation.setter
    def operation(self, value):
        assert isinstance(value, dict)
        self[1] = value

    @property
    def op(self):
        return self[1]

    def set(self, **data):
        try:
            class_ = self._class()
        except Exception:  # pragma: no cover
            raise NotImplementedError("Unimplemented Operation %s" % self.name)
        self.operation = class_(**data)

    def _setidanename(self, identifier):
        if isinstance(identifier, int):
            self.id = int(identifier)
            self.name = self.getOperationNameForId(self.id)
        else:
            assert identifier in self.ops
            self.id = self.getOperationIdForName(identifier)
            self.name = identifier

    @property
    def opId(self):
        return self.id

    @property
    def class_name(self):
        return self.name[0].upper() + self.name[1:]  # classname

    def _loadEchoObject(self, op):
        assert isinstance(op, EchoObject)
        self.operation = op
        self.name = op.__class__.__name__.lower()
        self.id = self.getOperationIdForName(self.name)

    def __bytes__(self):
        return bytes(Id(self.id)) + bytes(self.op)

    def __str__(self):
        return json.dumps(self.__json__())

    def __json__(self):
        return [self.id, self.op.json()]

    def _get_class(self, name):
        module = __import__(self.module, fromlist=self.fromlist)
        class_ = getattr(module, name)
        return class_

    def _class(self):
        return self._get_class(self.class_name)

    @property
    def ops(self):
        if callable(self.operations):
            # Legacy support
            return self.operations()
        else:
            return self.operations

    def getOperationIdForName(self, name):
        return self.ops[name]

    def getOperationNameForId(self, i):
        """ Convert an operation id into the corresponding string
        """
        for key in self.ops:
            if int(self.ops[key]) is int(i):
                return key
        raise ValueError("Unknown Operation ID %d" % i)

    toJson = __json__
    json = __json__


class EchoObject(OrderedDict):
    """ Core abstraction class

        This class is used for any JSON reflected object in ECHO.

        * ``instance.__json__()``: encodes data into json format
        * ``bytes(instance)``: encodes data into wire format
        * ``str(instances)``: dumps json object as string

    """

    def __init__(self, *args, **kwargs):
        if len(args) == 1 and isinstance(args[0], (dict, OrderedDict)):
            if hasattr(self, "detail"):
                super().__init__(self.detail(**args[0]))
            else:
                OrderedDict.__init__(self, args[0])
            return

        elif kwargs and hasattr(self, "detail"):
            # If I receive kwargs, I need detail() implemented!
            super().__init__(self.detail(*args, **kwargs))

    def __bytes__(self):
        if len(self) is 0:
            return bytes()
        b = b""
        for name, value in self.items():
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

    # Legacy support
    @property
    def data(self):  # pragma: no cover
        """ Read data explicitly (backwards compatibility)
        """
        return self

    @data.setter
    def data(self, data):  # pragma: no cover
        """ Set data through a setter (backwards compatibility)
        """
        self.update(data)

    toJson = __json__
    json = __json__


class ObjectId(ObjectIdParent):
    """ Need to overwrite a few attributes to load proper object_types from
        bitshares
    """

    object_types = object_type

"""
class AssetId(ObjectId):
    super().__init__(object_str="asset")


class AccountId(ObjectId):

    super().__init__(object_str="account")


class ContractId(ObjectId):

    super().__init__(object_str="contract")
"""


class Memo(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            prefix = default_prefix
            if "message" in kwargs and kwargs["message"]:
                super().__init__(
                    OrderedDict(
                        [
                            ("from", PublicKey(kwargs["from"], prefix=prefix)),
                            ("to", PublicKey(kwargs["to"], prefix=prefix)),
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
            prefix = default_prefix

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            kwargs["key_auths"] = sorted(
                kwargs["key_auths"],
                key=lambda x: PublicKey(x[0], prefix=prefix),
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
                    [PublicKey(e[0], prefix=prefix), Uint16(e[1])]
                    for e in kwargs["key_auths"]
                ]
            )
            super().__init__(
                OrderedDict(
                    [
                        ("weight_threshold", Uint32(int(kwargs["weight_threshold"]))),
                        ("account_auths", account_auths),
                        ("key_auths", key_auths),
                        ("extensions", Set([])),
                    ]
                )
            )


class AccountOptions(EchoObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        prefix = default_prefix

        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            # remove dublicates
            kwargs["votes"] = list(set(kwargs["votes"]))
            # Sort votes
            kwargs["votes"] = sorted(
                kwargs["votes"], key=lambda x: float(x.split(":")[1])
            )
            super().__init__(
                OrderedDict(
                    [
                        ("memo_key", PublicKey(kwargs["memo_key"], prefix=prefix)),
                        (
                            "voting_account",
                            ObjectId(kwargs["voting_account"], "account"),
                        ),
                        ("num_witness", Uint16(kwargs["num_witness"])),
                        ("num_committee", Uint16(kwargs["num_committee"])),
                        ("votes", Array([VoteId(o) for o in kwargs["votes"]])),
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


# Legacy
def isArgsThisClass(self, args):
    return len(args) == 1 and type(args[0]).__name__ == type(self).__name__


# Common Objects
class Asset(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            super().__init__(
                OrderedDict(
                    [
                        ("amount", Int64(kwargs["amount"])),
                        ("asset_id", ObjectId(kwargs["asset_id"], "asset")),
                    ]
                )
            )


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
                        ("echo_contract_id", ObjectId(kwargs["echo_contract_id"], "contract")),
                        ("echo_vote_method", String(kwargs["echo_vote_method"])),
                        ("echo_sign_method", String(kwargs["echo_sign_method"])),
                        ("echo_transfer_topic", String(kwargs["echo_transfer_topic"])),
                        ("echo_transfer_ready_topic", String(kwargs["echo_transfer_ready_topic"])),
                        ("eth_contract_address", String(kwargs["eth_contract_address"])),
                        ("eth_committee_method", String(kwargs["eth_committee_method"])),
                        ("eth_transfer_topic", String(kwargs["eth_transfer_topic"]))
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
                        ("maximum_asset_whitelist_authorities", Uint8(kwargs["maximum_asset_whitelist_authorities"])),
                        ("maximum_asset_feed_publishers", Uint8(kwargs["maximum_asset_feed_publishers"])),
                        ("maximum_witness_count", Uint16(kwargs["maximum_witness_count"])),
                        ("maximum_committee_count", Uint16(kwargs["maximum_committee_count"])),
                        ("maximum_authority_membership", Uint16(kwargs["maximum_authority_membership"])),
                        ("reserve_percent_of_fee", Uint16(kwargs["reserve_percent_of_fee"])),
                        ("network_percent_of_fee", Uint16(kwargs["network_percent_of_fee"])),
                        ("lifetime_referrer_percent_of_fee", Uint16(kwargs["lifetime_referrer_percent_of_fee"])),
                        ("cashback_vesting_period_seconds", Uint32(kwargs["cashback_vesting_period_seconds"])),
                        ("cashback_vesting_threshold", Int64(kwargs["cashback_vesting_threshold"])),
                        ("count_non_member_votes", Bool(kwargs["count_non_member_votes"])),
                        ("allow_non_member_whitelists", Bool(kwargs["allow_non_member_whitelists"])),
                        ("witness_pay_per_block", Int64(kwargs["witness_pay_per_block"])),
                        ("worker_budget_per_day", Int64(kwargs["worker_budget_per_day"])),
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
