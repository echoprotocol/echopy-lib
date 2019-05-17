# -*- coding: utf-8 -*-
from collections import OrderedDict
from .types import (
    Array,
    Bool,
    Bytes,
    FixedArray,
    Id,
    Int64,
    Map,
    Optional,
    PointInTime,
    Set,
    Signature,
    StaticVariant,
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
    AccountOptions,
    Asset,
    AssetOptions,
    BitAssetOptions,
    Memo,
    ObjectId,
    Permission,
    Price,
    PriceFeed,
    WorkerInitializer,
    isArgsThisClass,
    VestingPolicyInitializer,
    ChainParameters,
)

from .objects import EchoObject
from .account import PublicKey

from .operationids import operations
from functools import partial


class_idmap = {}
class_namemap = {}


def snake_to_camel(text):
    """Convert string in snake_case to camelCase."""
    text_parts = text.split('_')
    return ''.join(word.capitalize() for word in text_parts)


def camel_to_snake(text):
    """Convert string in camelCase to snake_case."""
    import re
    str1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', str1).lower()


def fill_classmaps():
    """Fill global dict's for get_operation_by_id and get_operation_by_name methods."""
    for name, ind in operations.items():
        classname = snake_to_camel(name)
        class_namemap[classname] = ind
        try:
            class_idmap[ind] = globals()[classname]
        except Exception:
            continue


def get_operation_by_id(op_id):
    """Convert an operation id into the (operation_id, corresponding class)."""
    return (op_id, class_idmap[op_id]) if op_id in class_idmap else (None, None)


def get_operation_by_name(op_name):
    """Convert an operation name into the (operation_id, coressponding class)."""
    _id = class_namemap[op_name]

    return _id, class_idmap[_id]


def get_optional(param, kwargs, object_class):
    """Wrapper for optional params init."""
    result = object_class(kwargs[param]) if param in kwargs else ''
    return result


class Transfer(EchoObject):
    def detail(self, *args, **kwargs):
        memo = get_optional("memo", kwargs, Memo)

        result = OrderedDict(
            [
                ("from", ObjectId(kwargs["from"], "account")),
                ("to", ObjectId(kwargs["to"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("memo", Optional(memo)),
                ("extensions", Set([])),

            ]
        )
        self.add_fee(result, kwargs)

        return result


class LimitOrderCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("seller", ObjectId(kwargs["seller"], "account")),
                ("amount_to_sell", Asset(kwargs["amount_to_sell"])),
                ("min_to_receive", Asset(kwargs["min_to_receive"])),
                ("expiration", PointInTime(kwargs["expiration"])),
                ("fill_or_kill", Bool(kwargs["fill_or_kill"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class LimitOrderCancel(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("order", ObjectId(kwargs["order"], "limit_order")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CallOrderUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("funding_account", ObjectId(kwargs["funding_account"], "account")),
                ("delta_collateral", Asset(kwargs["delta_collateral"])),
                ("delta_debt", Asset(kwargs["delta_debt"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class FillOrder(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("order_id", ObjectId(kwargs["order_id"])),
                ("account_id", ObjectId(kwargs["account_id"], "account")),
                ("pays", Asset(kwargs["pays"])),
                ("receives", Asset(kwargs["receives"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AccountCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("registrar", ObjectId(kwargs["registrar"], "account")),
                ("referrer", ObjectId(kwargs["referrer"], "account")),
                ("referrer_percent", Uint16(kwargs["referrer_percent"])),
                ("name", String(kwargs["name"])),
                ("active", Permission(kwargs["active"])),
                ("ed_key", PublicKey(kwargs["ed_key"])),
                ("options", AccountOptions(kwargs["options"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AccountUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        active = get_optional("active", kwargs, Permission)
        ed_key = get_optional("ed_key", kwargs, PublicKey)
        new_options = get_optional("new_options", kwargs, AccountOptions)

        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("active", Optional(active)),
                ("ed_key", Optional(ed_key)),
                ("new_options", Optional(new_options)),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AccountWhitelist(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("authorizing_account", ObjectId(kwargs["authorizing_account"], "account")),
                ("new_listing", Uint8(kwargs["new_listing"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AccountUpgrade(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account_to_upgrade", ObjectId(kwargs["account_to_upgrade"], "account")),
                ("upgrade_to_lifetime_member", Bool(kwargs["upgrade_to_lifetime_member"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AccountTransfer(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account_id", ObjectId(kwargs["account_id"], "account")),
                ("new_owner", ObjectId(kwargs["new_owner"], "account")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetCreate(EchoObject):
    def detail(self, *args, **kwargs):
        bitasset_opts = get_optional("bitasset_opts", kwargs, BitAssetOptions)

        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("symbol", String(kwargs["symbol"])),
                ("precision", Uint8(kwargs["precision"])),
                ("common_options", AssetOptions(kwargs["common_options"])),
                ("bitasset_opts", Optional(bitasset_opts)),
                ("is_prediction_market", Bool(kwargs["is_prediction_market"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        new_issuer = get_optional("new_issuer", kwargs, partial(ObjectId, type_verify="account"))

        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_update", ObjectId(kwargs["asset_to_update"], "asset")),
                ("new_issuer", Optional(new_issuer)),
                ("new_options", AssetOptions(kwargs["new_options"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetUpdateBitasset(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_update", ObjectId(kwargs["asset_to_update"], "asset")),
                ("new_options", BitAssetOptions(kwargs["new_options"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetUpdateFeedProducers(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_update", ObjectId(kwargs["asset_to_update"], "asset")),
                ("new_feed_producers", Set(ObjectId(kwargs["new_feed_producers"], "account"))),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetIssue(EchoObject):
    def detail(self, *args, **kwargs):
        memo = get_optional("memo", kwargs, Memo)

        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_issue", Asset(kwargs["asset_to_issue"])),
                ("issue_to_account", ObjectId(kwargs["issue_to_account"], "account")),
                ("memo", Optional(memo)),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetReserve(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("payer", ObjectId(kwargs["payer"], "account")),
                ("amount_to_reserve", Asset(kwargs["asset"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetFundFeePool(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("from_account", ObjectId(kwargs["from_account"], "account")),
                ("asset_id", ObjectId(kwargs["asset_id"], "asset")),
                ("amount", Int64(kwargs["amount"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetSettle(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("amount", Asset(kwargs["asset"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetGlobalSettle(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_settle", ObjectId(kwargs["asset_to_settle"], "asset")),
                ("settle_price", Price(kwargs["settle_price"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetPublishFeed(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("publisher", ObjectId(kwargs["publisher"], "account")),
                ("asset_id", ObjectId(kwargs["asset_id"], "asset")),
                ("feed", PriceFeed(kwargs["feed"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ProposalCreate(EchoObject):
    def detail(self, *args, **kwargs):
        review_period_seconds = get_optional("review_period_seconds", kwargs, Uint32)

        result = OrderedDict(
            [
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("expiration_time", PointInTime(kwargs["expiration_time"])),
                ("proposed_ops", Array(StaticVariant(kwargs["proposed_ops"]))),
                ("review_period_seconds", Optional(review_period_seconds)),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ProposalUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("proposal", ObjectId(kwargs["proposal"], "proposal")),
                ("active_approvals_to_add", Set(ObjectId(kwargs["active_approvals_to_add"], "account"))),
                ("active_approvals_to_remove", Set(ObjectId(kwargs["active_approvals_to_remove"], "account"))),
                ("owner_approvals_to_add", Set(ObjectId(kwargs["owner_approvals_to_add"], "account"))),
                ("owner_approvals_to_remove", Set(ObjectId(kwargs["owner_approvals_to_remove"], "account"))),
                ("key_approvals_to_add", Set(PublicKey(kwargs["key_approvals_to_add"]))),
                ("key_approvals_to_remove", Set(PublicKey(kwargs["key_approvals_to_remove"]))),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ProposalDelete(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("using_owner_authority", Bool(kwargs["using_owner_authority"])),
                ("proposal", ObjectId(kwargs["proposal"], "proposal")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class WithdrawPermissionCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("withdraw_from_account", ObjectId(kwargs["withdraw_from_account"], "account")),
                ("authorized_account", ObjectId(kwargs["authorized_account"], "account")),
                ("withdrawal_limit", Asset(kwargs["withdrawal_limit"])),
                ("withdrawal_period_sec", Uint32(kwargs["withdrawal_period_sec"])),
                ("periods_until_expiration", Uint32(kwargs["periods_until_expiration"])),
                ("period_start_time", PointInTime(kwargs["period_start_time"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class WithdrawPermissionUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("withdraw_from_account", ObjectId(kwargs["withdraw_from_account"], "account")),
                ("authorized_account", ObjectId(kwargs["authorized_account"], "account")),
                ("permission_to_update", ObjectId(kwargs["permission_to_update"], "withdraw_permission")),
                ("withdrawal_limit", Asset(kwargs["withdrawal_limit"])),
                ("withdrawal_period_sec", Uint32(kwargs["withdrawal_period_sec"])),
                ("period_start_time", PointInTime(kwargs["period_start_time"])),
                ("periods_until_expiration", Uint32(kwargs["periods_until_expiration"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class WithdrawPermissionClaim(EchoObject):
    def detail(self, *args, **kwargs):
        memo = get_optional("memo", kwargs, Memo)

        result = OrderedDict(
            [
                ("withdraw_permission", ObjectId(kwargs["withdraw_permission"], "withdraw_permission")),
                ("withdraw_from_account", ObjectId(kwargs["withdraw_from_account"], "account")),
                ("withdraw_to_account", ObjectId(kwargs["withdraw_to_account"], "account")),
                ("amount_to_withdraw", Asset(kwargs["amount_to_withdraw"])),
                ("memo", Optional(memo)),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class WithdrawPermissionDelete(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("withdraw_from_account", ObjectId(kwargs["withdraw_from_account"], "account")),
                ("authorized_account", ObjectId(kwargs["authorized_account"], "account")),
                ("withdrawal_permission", ObjectId(kwargs["withdrawal_permission"], "withdraw_permission")),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeMemberCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("committee_member_account", ObjectId(kwargs["committee_member_account"], "account")),
                ("url", String(kwargs["url"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeMemberUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        new_url = get_optional("new_url", kwargs, String)

        result = OrderedDict(
            [
                ("committee_member", ObjectId(kwargs["committee_member"], "committee_member")),
                ("committee_member_account", ObjectId(kwargs["committee_member_account"], "account")),
                ("new_url", Optional(new_url)),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeMemberUpdateGlobalParameters(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("new_parameters", ChainParameters(kwargs["new_parameters"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class VestingBalanceCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("creator", ObjectId(kwargs["creator"], "account")),
                ("owner", ObjectId(kwargs["owner"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("policy", VestingPolicyInitializer(kwargs["policy"]))
            ]
        )
        self.add_fee(result, kwargs)

        return result


class VestingBalanceWithdraw(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("vesting_balance", ObjectId(kwargs["vesting_balance"], "vesting_balance")),
                ("owner", ObjectId(kwargs["owner"], "account")),
                ("amount", Asset(kwargs["amount"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class Custom(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("payer", ObjectId(kwargs["payer"], "account")),
                ("required_auths", Set(ObjectId(kwargs["required_auths"], "account"))),
                ("id", Uint16(kwargs["id"])),
                ("data", Bytes(kwargs["data"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class Assert(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("predicates", Array(kwargs["predicates"])),
                ("required_auths", Set(ObjectId(kwargs["required_auths"], "account"))),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class BalanceClaim(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("deposit_to_account", ObjectId(kwargs["deposit_to_account"], "account")),
                ("balance_to_claim", ObjectId(kwargs["balance_to_claim"], "balance")),
                ("balance_owner_key", PublicKey(kwargs["balance_owner_key"])),
                ("total_claimed", Asset(kwargs["total_claimed"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class OverrideTransfer(EchoObject):
    def detail(self, *args, **kwargs):
        memo = get_optional("memo", kwargs, Memo)

        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("from", ObjectId(kwargs["from"], "account")),
                ("to", ObjectId(kwargs["to"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("memo", Optional(memo)),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetSettleCancel(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("settlement", ObjectId(kwargs["settlement"], "force_settlement")),
                ("account", ObjectId(kwargs["account"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetClaimFees(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("amount_to_claim", Asset(kwargs["amount_to_claim"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class BidCollateral(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("bidder", ObjectId(kwargs["bidder"], "account")),
                ("additional_collateral", Asset(kwargs["additional_collateral"])),
                ("debt_covered", Asset(kwargs["debt_covered"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ExecuteBid(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("bidder", ObjectId(kwargs["bidder"], "account")),
                ("debt", Asset(kwargs["debt"])),
                ("collateral", Asset(kwargs["collateral"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CreateContract(EchoObject):
    def detail(self, *args, **kwargs):
        supported_asset_id = get_optional("supported_asset_id", kwargs, partial(ObjectId, type_verify="asset"))

        result = OrderedDict(
            [
                ("registrar", ObjectId(kwargs["registrar"], "account")),
                ("value", Asset(kwargs["value"])),
                ("code", String(kwargs["code"])),
                ("supported_asset_id", Optional(supported_asset_id)),
                ("eth_accuracy", Bool(kwargs["eth_accuracy"])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CallContract(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("registrar", ObjectId(kwargs["registrar"], "account")),
                ("value", Asset(kwargs["value"])),
                ("code", String(kwargs["code"])),
                ("callee", ObjectId(kwargs["callee"], "contract")),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ContractTransfer(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("from", ObjectId(kwargs["account"], "account")),
                ("to", ObjectId(kwargs["account"], "account")),
                ("amount", Asset(kwargs["asset"])),
                ("extensions", Set([])),

            ]
        )
        self.add_fee(result, kwargs)

        return result


class AccountAddressCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("owner", ObjectId(kwargs["owner"], "account")),
                ("label", String(kwargs["label"])),
                ("extensions", Set([])),

            ]
        )
        self.add_fee(result, kwargs)

        return result


class TransferToAddress(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("from", ObjectId(kwargs["from"], "account")),
                ("to", String(kwargs["to"])),
                ("amount", Asset(kwargs["amount"]))
                ("extensions", Set([])),

            ]
        )
        self.add_fee(result, kwargs)

        return result


class GenerateEthAddress(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account_id", ObjectId(kwargs["account_id"], "account")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class WithdrawEth(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("acc_id", ObjectId(kwargs["acc_id"], "account")),
                ("eth_addr", String(kwargs["eth_addr"])),
                ("value", Uint64(kwargs["value"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


fill_classmaps()
