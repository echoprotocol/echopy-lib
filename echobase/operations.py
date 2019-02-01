# -*- coding: utf-8 -*-
from collections import OrderedDict
from .types import (
    Array,
    Bool,
    Bytes,
    Fixed_array,
    Id,
    Int16,
    Int64,
    Map,
    Optional,
    PointInTime,
    Set,
    Signature,
    Static_variant,
    String,
    Uint8,
    Uint16,
    Uint32,
    Uint64,
    Varint32,
    Void,
    VoteId,
)

from .objects import (
    AccountCreateExtensions,
    AccountOptions,
    Asset,
    AssetOptions,
    BitAssetOptions,
    CallOrderExtension,
    Memo,
    ObjectId,
    Operation,
    Permission,
    Price,
    PriceFeed,
    SpecialAuthority,
    Worker_initializer,
    isArgsThisClass,
)

from .objects import EchoObject
from .account import PublicKey
from .chains import default_prefix


# Old style of defining an operation
class Demooepration(EchoObject):
    def __init__(self, *args, **kwargs):
        if isArgsThisClass(self, args):  # pragma: no cover
            self.data = args[0].data
        else:
            if len(args) == 1 and len(kwargs) == 0:
                kwargs = args[0]  # pragma: no cover
            super().__init__(
                OrderedDict(
                    [("string", String(kwargs["string"])), ("extensions", Set([]))]
                )
            )


# New style of defining operation
class Newdemooepration(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("string", String(kwargs["string"])),
                ("optional", Optional(String(kwargs.get("optional")))),
                ("extensions", Set([])),
            ]
        )


class Newdemooepration2(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                # Different order
                ("optional", Optional(String(kwargs.get("optional")))),
                ("string", String(kwargs["string"])),
                ("extensions", Set([])),
            ]
        )


# For more detailed unit testing
class Account_create(EchoObject):
    def detail(self, *args, **kwargs):
        prefix = kwargs.get("prefix", default_prefix)
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("registrar", ObjectId(kwargs["registrar"], "account")),
                ("referrer", ObjectId(kwargs["referrer"], "account")),
                ("referrer_percent", Uint16(kwargs["referrer_percent"])),
                ("name", String(kwargs["name"])),
                ("owner", Permission(kwargs["owner"], prefix=prefix)),
                ("active", Permission(kwargs["active"], prefix=prefix)),
                ("options", AccountOptions(kwargs["options"], prefix=prefix)),
                ("extensions", Set([])),
            ]
        )
