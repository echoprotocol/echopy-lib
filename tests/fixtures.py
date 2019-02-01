# -*- coding: utf-8 -*-
import os
import mock
import yaml

# Echo API
from echoapi import exceptions
from echoapi.api import Api, Websocket, Http

# Echobase
import echobase.ecdsa as ecdsa
from echobase.aes import AESCipher
from echobase.base58 import (
    Base58,
    base58decode,
    base58encode,
    ripemd160,
    base58CheckEncode,
    base58CheckDecode,
    gphBase58CheckEncode,
    gphBase58CheckDecode,
    b58decode,
    b58encode,
)
from echobase import types, utils
from echobase.transactions import formatTimeFromNow, timeformat
from echobase.operations import Account_create
from echobase.signedtransactions import Signed_Transaction, MissingSignatureForKey
from echobase.account import (
    BrainKey,
    Address,
    PublicKey,
    PrivateKey,
    PasswordKey,
    EchoAddress,
    BitcoinAddress,
)
from echobase.objects import Operation, EchoObject
from echobase.operations import Newdemooepration, Newdemooepration2, Demooepration
from echobase.operationids import ops, operations, getOperationNameForId

from echobase import bip38
from echobase.bip38 import encrypt, decrypt
from echobase.transactions import getBlockParams

# Echostorage
from echostorage.exceptions import (
    WrongMasterPasswordException,
    KeyAlreadyInStoreException,
    WalletLocked,
)
import echostorage as storage
from echostorage.interfaces import (
    StoreInterface,
    KeyInterface,
    ConfigInterface,
    EncryptedKeyInterface,
)
from echostorage.sqlite import SQLiteStore


# Common stuff

from echocommon.instance import (
    BlockchainInstance as GBlockchainInstance,
    SharedInstance as GSharedInstance,
)
from echocommon.amount import Amount as GAmount
from echocommon.account import Account as GAccount, AccountUpdate as GAccountUpdate
from echocommon.asset import Asset as GAsset
from echocommon.committee import Committee as GCommittee
from echocommon.block import Block as GBlock, BlockHeader as GBlockHeader
from echocommon.message import Message as GMessage
from echocommon.blockchainobject import ObjectCache, BlockchainObject
from echocommon.price import Price as GPrice
from echocommon.wallet import Wallet as GWallet
from echocommon.worker import Worker as GWorker, Workers as GWorkers
from echocommon.witness import Witness as GWitness, Witnesses as GWitnesss
from echocommon.chain import AbstractEchoChain


class SharedInstance(GSharedInstance):
    pass


class Chain(AbstractEchoChain):
    prefix = "GPH"

    def __init__(self, *args, **kwargs):
        self.config = storage.InRamConfigurationStore()
        self.blockchainobject_class = BlockchainObject

    def is_connected(self):
        return True

    @property
    def wallet(self):
        return Wallet(keys=["5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"])

    def info(self):
        # returns demo data
        return {
            "accounts_registered_this_interval": 18,
            "current_aslot": 33206892,
            "current_witness": "1.6.105",
            "dynamic_flags": 0,
            "head_block_id": "01f82b16db7ae25a4b9706b36c259438a9d4c8d1",
            "head_block_number": 33041174,
            "id": "2.1.0",
            "last_budget_time": "2018-12-12T10:00:00",
            "last_irreversible_block_num": 33041151,
            "next_maintenance_time": "2018-12-12T11:00:00",
            "recent_slots_filled": "340282366920938463463374607431768211455",
            "recently_missed_count": 0,
            "time": "2018-12-12T10:44:15",
            "witness_budget": 31800000,
        }

    @property
    def rpc(self):
        """ We are patching rpc similar to a regular RPC
            connection. However, it will always return
            an empty object!
        """

        class RPC:
            def _load(self, name):
                with open(
                    os.path.join(os.path.dirname(__file__), "fixtures.yaml")
                ) as fid:
                    d = yaml.safe_load(fid)
                return d.get(name)

            def get_objects(self, *args, **kwargs):
                return []

            def get_object(self, *args, **kwargs):
                return {}

            def get_account_history(self, *args, **kwargs):
                return []

            def lookup_account_names(self, name, **kwargs):
                return [None]

            def get_all_workers(self):
                return self._load("workers")

            def get_workers_by_account(self, name):
                return [self._load("workers")[0]]

            def __getattr__(self, name):
                def fun(self, *args, **kwargs):
                    return {}

                return fun

        return RPC()

    def upgrade_account(self, *args, **kwargs):
        pass


class BlockchainInstance(GBlockchainInstance):
    def get_instance_class(self):
        return Chain


@BlockchainInstance.inject
class Asset(GAsset):
    def define_classes(self):
        self.type_id = 3


@BlockchainInstance.inject
class Amount(GAmount):
    def define_classes(self):
        self.asset_class = Asset
        self.price_class = Price


@BlockchainInstance.inject
class Account(GAccount):
    def define_classes(self):
        self.type_id = 2
        self.amount_class = Amount
        self.operations = operations


@BlockchainInstance.inject
class AccountUpdate(GAccountUpdate):
    def define_classes(self):
        self.account_class = Account


@BlockchainInstance.inject
class Committee(GCommittee):
    def define_classes(self):
        self.type_id = 5
        self.account_class = Account


@BlockchainInstance.inject
class Block(GBlock):
    def define_classes(self):
        pass


@BlockchainInstance.inject
class BlockHeader(GBlockHeader):
    def define_classes(self):
        pass


@BlockchainInstance.inject
class Message(GMessage):
    def define_classes(self):
        self.account_class = Account
        self.publickey_class = PublicKey


@BlockchainInstance.inject
class Price(GPrice):
    def define_classes(self):
        self.asset_class = Asset
        self.amount_class = Amount


@BlockchainInstance.inject
class Wallet(GWallet):
    def define_classes(self):
        self.default_key_store_app_name = "echo"
        self.privatekey_class = PrivateKey


@BlockchainInstance.inject
class Worker(GWorker):
    def define_classes(self):
        self.type_id = 14
        self.account_class = Account


@BlockchainInstance.inject
class Workers(GWorkers):
    def define_classes(self):
        self.worker_class = Worker
        self.account_class = Account


@BlockchainInstance.inject
class Witness(GWitness):
    def define_classes(self):
        self.type_id = 6
        self.account_class = Account


@BlockchainInstance.inject
class Witnesses(GWitnesss):
    def define_classes(self):
        self.witness_class = Witness
        self.account_class = Account


def fixture_data():
    with open(os.path.join(os.path.dirname(__file__), "fixtures.yaml")) as fid:
        data = yaml.safe_load(fid)

    # Feed our objects into the caches!
    for account in data.get("accounts"):
        Account._cache[account["id"]] = account
        Account._cache[account["name"]] = account

    for asset in data.get("assets"):
        Asset._cache[asset["symbol"]] = asset
        Asset._cache[asset["id"]] = asset

    for committee in data.get("committees"):
        Committee._cache[committee["id"]] = committee

    for blocknum, block in data.get("blocks").items():
        block["id"] = blocknum
        Block._cache[str(blocknum)] = block

    for worker in data.get("workers"):
        Worker._cache[worker["id"]] = worker

    for witness in data.get("witnesses"):
        Witness._cache[witness["id"]] = witness
