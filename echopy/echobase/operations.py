# -*- coding: utf-8 -*-
from collections import OrderedDict
from .types import (
    Array,
    Bool,
    Bytes,
    Int64,
    Optional,
    PointInTime,
    Set,
    StaticVariant,
    String,
    Uint8,
    Uint16,
    Uint32,
    Uint64,
    Map
)

from .objects import (
    AccountOptions,
    Asset,
    AssetOptions,
    BitAssetOptions,
    ObjectId,
    Permission,
    Price,
    PriceFeed,
    VestingPolicyInitializer,
    ChainParameters,
    OpWrapper,
    BtcTransactionDetails,
    P2shP2wsh,
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


# Asset Transfer
class Transfer(EchoObject):
    def detail(self, *args, **kwargs):

        result = OrderedDict(
            [
                ("from", ObjectId(kwargs["from"], "account")),
                ("to", ObjectId(kwargs["to"], "account")),
                ("amount", Asset(kwargs["amount"])),
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
                ("to", Bytes(kwargs["to"], 20)),
                ("amount", Asset(kwargs["amount"])),
                ("extensions", Set([])),

            ]
        )
        self.add_fee(result, kwargs)

        return result


class OverrideTransfer(EchoObject):
    def detail(self, *args, **kwargs):

        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("from", ObjectId(kwargs["from"], "account")),
                ("to", ObjectId(kwargs["to"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


# Account Management
class AccountCreate(EchoObject):
    def detail(self, *args, **kwargs):
        evm_address = get_optional("evm_address", kwargs, Bytes)
        result = OrderedDict(
            [
                ("registrar", ObjectId(kwargs["registrar"], "account")),
                ("name", String(kwargs["name"])),
                ("active", Permission(kwargs["active"])),
                ("echorand_key", PublicKey(kwargs["echorand_key"])),
                ("evm_address", Optional(evm_address)),
                ("options", AccountOptions(kwargs["options"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AccountUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        active = get_optional("active", kwargs, Permission)
        echorand_key = get_optional("echorand_key", kwargs, PublicKey)
        new_options = get_optional("new_options", kwargs, AccountOptions)

        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("active", Optional(active)),
                ("echorand_key", Optional(echorand_key)),
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
                ("account_to_list", ObjectId(kwargs["account_to_list"], "account")),
                ("new_listing", Uint8(kwargs["new_listing"])),
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


# Asset Management
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
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        new_issuer = get_optional("new_issuer", kwargs, partial(ObjectId, type_verify="account"))
        new_options = get_optional("new_options", kwargs, AssetOptions)

        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_update", ObjectId(kwargs["asset_to_update"], "asset")),
                ("new_issuer", Optional(new_issuer)),
                ("new_options", Optional(new_options)),
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
                ("new_feed_producers", Set([ObjectId(i, "account") for i in kwargs["new_feed_producers"]])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class AssetIssue(EchoObject):
    def detail(self, *args, **kwargs):

        result = OrderedDict(
            [
                ("issuer", ObjectId(kwargs["issuer"], "account")),
                ("asset_to_issue", Asset(kwargs["asset_to_issue"])),
                ("issue_to_account", ObjectId(kwargs["issue_to_account"], "account")),
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
                ("amount_to_reserve", Asset(kwargs["amount_to_reserve"])),
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


# Proposals
class ProposalCreate(EchoObject):
    def detail(self, *args, **kwargs):
        review_period_seconds = get_optional("review_period_seconds", kwargs, Uint32)
        proposed_operations = []
        for proposed_operation in kwargs["proposed_ops"]:
            operation_id, operation_class = get_operation_by_id(proposed_operation[0])
            proposed_operations.append(OpWrapper(op=[operation_id, operation_class(proposed_operation[1])]))
        result = OrderedDict(
            [
                ("fee_paying_account", ObjectId(kwargs["fee_paying_account"], "account")),
                ("expiration_time", PointInTime(kwargs["expiration_time"])),
                ("proposed_ops", Array(proposed_operations)),
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
                ("active_approvals_to_add", Set([ObjectId(i, "account") for i in
                                                 kwargs["active_approvals_to_add"]])),
                ("active_approvals_to_remove", Set([ObjectId(i, "account") for i in
                                                    kwargs["active_approvals_to_remove"]])),
                ("key_approvals_to_add", Set([PublicKey(i) for i in kwargs["key_approvals_to_add"]])),
                ("key_approvals_to_remove", Set([PublicKey(i) for i in kwargs["key_approvals_to_remove"]])),
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


# Committee Member
class CommitteeMemberCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("committee_member_account", ObjectId(kwargs["committee_member_account"], "account")),
                ("url", String(kwargs["url"])),
                ("eth_address", Bytes(kwargs["eth_address"])),
                ("btc_public_key", Bytes(kwargs["btc_public_key"], 33)),
                ("deposit", Asset(kwargs["deposit"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeMemberUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        new_url = get_optional("new_url", kwargs, String)
        new_eth_address = get_optional("new_eth_address", kwargs, partial(Bytes))
        new_btc_public_key = get_optional("new_btc_public_key", kwargs, partial(Bytes, length=33))

        result = OrderedDict(
            [
                ("committee_member", ObjectId(kwargs["committee_member"], "committee_member")),
                ("committee_member_account", ObjectId(kwargs["committee_member_account"], "account")),
                ("new_url", Optional(new_url)),
                ("new_eth_address", Optional(new_eth_address)),
                ("new_btc_public_key", Optional(new_btc_public_key)),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeMemberUpdateGlobalParameters(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("new_parameters", ChainParameters(kwargs["new_parameters"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeMemberActivate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("committee_to_activate", ObjectId(kwargs["committee_to_activate"], "committee_member")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeMemberDeactivate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("committee_to_deactivate", ObjectId(kwargs["committee_to_deactivate"], "committee_member")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeFrozenBalanceDeposit(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("committee_member_account", ObjectId(kwargs["committee_member_account"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class CommitteeFrozenBalanceWithdraw(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("committee_member_account", ObjectId(kwargs["committee_member_account"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


# Vesting Balances
class VestingBalanceCreate(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("creator", ObjectId(kwargs["creator"], "account")),
                ("owner", ObjectId(kwargs["owner"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("policy", VestingPolicyInitializer(kwargs["policy"])),
                ("extensions", Set([])),
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
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


# Balance Object
class BalanceClaim(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("deposit_to_account", ObjectId(kwargs["deposit_to_account"], "account")),
                ("balance_to_claim", ObjectId(kwargs["balance_to_claim"], "balance")),
                ("balance_owner_key", PublicKey(kwargs["balance_owner_key"])),
                ("total_claimed", Asset(kwargs["total_claimed"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class BalanceFreeze(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("duration", Uint16(kwargs["duration"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class BalanceUnfreeze(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("amount", Asset(kwargs["amount"])),
                ("extensions", Set([])),
            ]
        )
        return result


# Contracts
class ContractCreate(EchoObject):
    def detail(self, *args, **kwargs):
        supported_asset_id = get_optional("supported_asset_id", kwargs, partial(ObjectId, type_verify="asset"))

        result = OrderedDict(
            [
                ("registrar", ObjectId(kwargs["registrar"], "account")),
                ("value", Asset(kwargs["value"])),
                ("code", String(kwargs["code"])),
                ("supported_asset_id", Optional(supported_asset_id)),
                ("eth_accuracy", Bool(kwargs["eth_accuracy"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ContractCall(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("registrar", ObjectId(kwargs["registrar"], "account")),
                ("value", Asset(kwargs["value"])),
                ("code", String(kwargs["code"])),
                ("callee", ObjectId(kwargs["callee"], "contract")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ContractUpdate(EchoObject):
    def detail(self, *args, **kwargs):
        new_owner = get_optional("new_owner", kwargs, partial(ObjectId, type_verify="account"))
        result = OrderedDict(
            [
                ("sender", ObjectId(kwargs["sender"], "account")),
                ("contract", ObjectId(kwargs["contract"], "contract")),
                ("new_owner", Optional(new_owner)),
                ("extensions", Set([])),

            ]
        )
        self.add_fee(result, kwargs)

        return result


class ContractFundPool(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("sender", ObjectId(kwargs["sender"], "account")),
                ("contract", ObjectId(kwargs["contract"], "contract")),
                ("value", Asset(kwargs["value"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class ContractWhitelist(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("sender", ObjectId(kwargs["sender"], "account")),
                ("contract", ObjectId(kwargs["contract"], "contract")),
                ("add_to_whitelist", Set([ObjectId(i, "account") for i in kwargs["add_to_whitelist"]])),
                ("remove_from_whitelist", Set([ObjectId(i, "account") for i in kwargs["remove_from_whitelist"]])),
                ("add_to_blacklist", Set([ObjectId(i, "account") for i in kwargs["add_to_blacklist"]])),
                ("remove_from_blacklist", Set([ObjectId(i, "account") for i in kwargs["remove_from_blacklist"]])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


# Sidechain (Ethereum)
class SidechainEthCreateAddress(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class SidechainEthWithdraw(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("eth_addr", Bytes(kwargs["eth_addr"])),
                ("value", Uint64(kwargs["value"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


# Sidechain (ERC20)
class SidechainErc20RegisterToken(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("eth_addr", Bytes(kwargs["eth_addr"])),
                ("name", String(kwargs["name"])),
                ("symbol", String(kwargs["symbol"])),
                ("decimals", Uint8(kwargs["decimals"])),
                ("extensions", Set([])),

            ]
        )
        self.add_fee(result, kwargs)

        return result


class SidechainErc20WithdrawToken(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("to", Bytes(kwargs["to"])),
                ("erc20_token", ObjectId(kwargs["erc20_token"], "erc20_token")),
                ("value", String(kwargs["value"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


# Sidechain (Bitcoin)
class SidechainBtcCreateAddress(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("backup_address", String(kwargs["backup_address"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class SidechainBtcWithdraw(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("account", ObjectId(kwargs["account"], "account")),
                ("btc_addr", String(kwargs["btc_addr"])),
                ("value", Uint64(kwargs["value"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


class EvmAddressRegister(EchoObject):
    def detail(self, *args, **kwargs):
        result = OrderedDict(
            [
                ("owner", ObjectId(kwargs["owner"], "account")),
                ("evm_address", Bytes(kwargs["evm_address"])),
                ("extensions", Set([])),
            ]
        )
        self.add_fee(result, kwargs)

        return result


fill_classmaps()
