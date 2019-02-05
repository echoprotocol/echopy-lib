# -*- coding: utf-8 -*-
import json

from collections import OrderedDict
from echobase.types import (
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
    Fixed_array,
    Optional,
    Static_variant,
    Map,
    Id,
    VoteId,
    JsonObj,
)
from echobase.types import ObjectId as ObjectIdParent
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
        d = {}  # JSON output is *not* ordered
        for name, value in self.items():
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
            prefix = kwargs.pop("prefix", default_prefix)
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
            prefix = kwargs.pop("prefix", default_prefix)

            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]
            kwargs["key_auths"] = sorted(
                kwargs["key_auths"],
                key=lambda x: PublicKey(x[0], prefix=prefix),
                reverse=False,
            )
            accountAuths = Map(
                [
                    [ObjectId(e[0], "account"), Uint16(e[1])]
                    for e in kwargs["account_auths"]
                ]
            )
            keyAuths = Map(
                [
                    [PublicKey(e[0], prefix=prefix), Uint16(e[1])]
                    for e in kwargs["key_auths"]
                ]
            )
            super().__init__(
                OrderedDict(
                    [
                        ("weight_threshold", Uint32(int(kwargs["weight_threshold"]))),
                        ("account_auths", accountAuths),
                        ("key_auths", keyAuths),
                        ("extensions", Set([])),
                    ]
                )
            )


class AccountOptions(EchoObject):
    def __init__(self, *args, **kwargs):
        # Allow for overwrite of prefix
        prefix = kwargs.pop("prefix", default_prefix)

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
