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
    # AccountCreateExtensions,
    AccountOptions,
    Asset,
    AssetOptions,
    BitAssetOptions,
    # CallOrderExtension,
    Memo,
    ObjectId,
    Operation,
    Permission,
    Price,
    PriceFeed,
    # SpecialAuthority,
    # Worker_initializer,
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


class Account_update(EchoObject):
    def detail(self, *args, **kwargs):
        prefix = kwargs.get("prefix", default_prefix)
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("account", ObjectId(kwargs["account"], "account")),
                ("owner", Optional(Permission(kwargs["owner"], prefix=prefix))),
                ("active", Optional(Permission(kwargs["active"], prefix=prefix))),
                ("new_options", Optional(AccountOptions(kwargs["new_options"], prefix=prefix))),
                ("extensions", Optional(Set([]))),
            ]
        )


class Account_whitelist(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("authorizing_account", ObjectId(kwargs["authorizing_account"], "account")),
                ("new_listing", Uint8(kwargs["new_listing"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Assert(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("predicates", Array(kwargs["predicates"])),
                ("required_auths", Set(ObjectId(kwargs["required_auths"], "account"))),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_create(EchoObject):
    def detail(self, *args, **kwargs):
        prefix = kwargs.get("prefix", default_prefix)
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("symbol", String(kwargs["symbol"])),
                ("precision", Uint8(kwargs["precision"])),
                ("common_options", AssetOptions(kwargs["asset"], prefix=prefix)),
                ("bitasset_opts", Optional(BitAssetOptions(kwargs["bitasset_opts"], prefix=prefix))),
                ("is_prediction_market", Bool(kwargs["is_prediction_market"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_update(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_update", ObjectId(kwargs["asset_to_update"], "asset")),
                ("new_issuer", Optional(ObjectId(kwargs["new_issuer"], "account"))),
                ("new_options", AssetOptions(kwargs["new_options"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_update_bitasset(EchoObject):
    def detail(self, *args, **kwargs):
        prefix = kwargs.get("prefix", default_prefix)

        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_update", ObjectId(kwargs["asset_to_update"], "asset")),
                ("new_options", BitAssetOptions(kwargs["new_options"], prefix=prefix)),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_update_fee_producer(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_update", ObjectId(kwargs["asset_to_update"], "asset")),
                ("new_feed_producers", Set(ObjectId(kwargs["new_feed_producers"], "account"))),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_issue(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_issue", Asset(kwargs["asset_to_issue"])),
                ("issue_to_account", ObjectId(kwargs["issue_to_account"], "account")),
                ("memo", Optional(Memo(kwargs["memo"]))),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_reverse(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("payer", ObjectId(kwargs["payer"], "account")),
                ("amount_to_reserve", Asset(kwargs["asset"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_fund_fee_pool(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("from_account", ObjectId(kwargs["from_account"], "account")),
                ("asset_id", ObjectId(kwargs["asset_id"], "asset")),
                ("amount", Int64(kwargs["amount"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_settle(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("account", ObjectId(kwargs["account"], "account")),
                ("amount", Asset(kwargs["asset"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_global_settle(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_settle", ObjectId(kwargs["asset_to_settle"], "asset")),
                ("settle_price", Price(kwargs["settle_price"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_publish_feed(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("publisher", ObjectId(kwargs["publisher"], "account")),
                ("asset_id", ObjectId(kwargs["asset_id"], "asset")),
                ("feed", PriceFeed(kwargs["feed"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_settle_cancel(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("settlement", ObjectId(kwargs["settlement"], "FORCE_SETTLEMENT")),
                ("account", ObjectId(kwargs["account"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Asset_claim_fees(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("amount_to_claim", Asset(kwargs["amount_to_claim"])),
                ("extensions", Optional(Set([]))),
            ]
        )


class Balance_claim(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("deposit_to_account", ObjectId(kwargs["deposit_to_account"], "account")),
                ("balance_to_claim", ObjectId(kwargs["balance_to_claim"], "account")),
                ("balance_owner_key", PublicKey(kwargs["balance_owner_key"])),
                ("total_claimed", Asset(kwargs["total_claimed"])),
            ]
        )


def Transfer_to_blind(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("amount", Asset(kwargs["amount"])),
                ("from", ObjectId(kwargs["from"], "account")),
                ("blinding_factor", Bytes(32)),
                ("outputs", Array(kwargs["blindOutput"])),
            ]
        )


class Blind_transfer(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["asset"])),
                ("inputs", Array(kwargs["blindInput"])),
                ("outputs", Array(kwargs["blindOutput"])),
            ]
        )


class Transfer_from_blind(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["asset"])),
                ("amount", Asset(kwargs["amount"])),
                ("to", ObjectId(kwargs["to"], "account")),
                ("blinding_factor", Bytes(32)),
                ("inputs", Array(kwargs["blindInput"])),
            ]
        )


def Proposal_create(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("expiration_time", PointInTime(kwargs["expiration_time"])),
                ("proposed_ops", Array(Static_variant(kwargs["proposed_ops"]))),
                ("review_period_seconds", Optional(Uint32(kwargs["review_period_seconds"]))),
                ("extensions", Optional(Set([]))),
            ]
        )


def Proposal_update(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("proposal", ObjectId(kwargs["proposal"], "proposal")),
                ("active_approvals_to_add", Set(ObjectId(kwargs["active_approvals_to_add"], "account"))),
                ("active_approvals_to_remove", Set(ObjectId(kwargs["active_approvals_to_remove"], "account"))),
                ("owner_approvals_to_add", Set(ObjectId(kwargs["owner_approvals_to_add"], "account"))),
                ("owner_approvals_to_remove", Set(ObjectId(kwargs["owner_approvals_to_remove"], "account"))),
                ("key_approvals_to_add", Set(PublicKey(kwargs["key_approvals_to_add"]))),
                ("key_approvals_to_remove", Set(PublicKey(kwargs["key_approvals_to_remove"]))),
                ("extensions", Optional(Set([]))),
            ]
        )


def Proposal_delete(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("fee", Asset(kwargs["fee"])),
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("using_owner_authority", Bool(kwargs["using_owner_authority"])),
                ("proposal", ObjectId(kwargs["proposal"], "proposal")),
                ("extensions", Optional(Set([]))),
            ]
        )
