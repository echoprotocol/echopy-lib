from .echoapi import Api

from .echobase.operations import get_operation_by_id, get_operation_by_name
from .echobase.account import PrivateKey
from .echobase.objects import EchoObject, StaticVariant, Asset, ObjectId
from .echobase.types import Uint16, Uint32, PointInTime, Array, Set, Bytes

from collections import OrderedDict
from copy import copy

from math import ceil
from codecs import decode

from datetime import timezone, datetime
from calendar import timegm
import time

from .echobase.crypto import Crypto


echo_asset_id = '1.3.0'


class TransactionType(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("ref_block_num", Uint16(kwargs['ref_block_num'])),
                ("ref_block_prefix", Uint32(kwargs['ref_block_prefix'])),
                ("expiration", PointInTime(kwargs['expiration'])),
                ("operations", Array([StaticVariant(op_id, op) for op_id, op in kwargs['operations']])),
                ("extensions", Set([])),
            ]

        )


class SignedTransactionType(EchoObject):
    def detail(self, *args, **kwargs):
        return OrderedDict(
            [
                ("ref_block_num", Uint16(kwargs['ref_block_num'])),
                ("ref_block_prefix", Uint32(kwargs['ref_block_prefix'])),
                ("expiration", PointInTime(kwargs['expiration'])),
                ("operations", Array([StaticVariant(op_id, op) for op_id, op in kwargs['operations']])),
                ("extensions", Set([])),
                ("signatures", Array([Bytes(signature, 64) for signature in kwargs['signatures']])),
            ]
        )


class Transaction:

    def __init__(self, api):
        self.api = api
        self._operations = []
        self._operations_classes = []
        self._signers = []
        self._signatures = []
        self._finalized = False
        self._expiration = None
        self._ref_block_num = None
        self._ref_block_prefix = None
        self._chain_id = None
        self._crypto = Crypto

    @staticmethod
    def is_hex(s):
        try:
            int(s, 16)
            return True
        except ValueError:
            return False

    @staticmethod
    def bytes_to_int(_bytes):
        result = 0
        for b in _bytes:
            result = result * 256 + int(b)
        return result

    @property
    def ref_block_num(self):
        return self._ref_block_num

    @ref_block_num.setter
    def ref_block_num(self, value):
        if not isinstance(value, int):
            raise Exception('ref_block_num is not a int instance')
        if value < 0 or value > 0xffff:
            raise Exception('ref_block_num is not safe')
        self._ref_block_num = value

    @property
    def ref_block_prefix(self):
        return self._ref_block_prefix

    @ref_block_prefix.setter
    def ref_block_prefix(self, value):
        if isinstance(value, str) and self.is_hex(value):
            self._ref_block_prefix = self.bytes_to_int(bytes.fromhex(value)[:4])
            return
        if isinstance(value, int) and value > 0 and value < 2**32:
            self._ref_block_prefix = value
            return
        raise Exception('invalid ref_block_prefix format')

    @property
    def chain_id(self):
        return self._chain_id

    @chain_id.setter
    def chain_id(self, value):
        if isinstance(value, str) and self.is_hex(value) and len(value) == 64:
            self._chain_id = value
            return
        raise Exception('invalid chain_id format or length')

    @property
    def operations(self):
        def depth_copy(op):
            new_op = copy(op)
            for key in op.__dict__:
                new_op[key] = copy(op[key])
                if hasattr(op[key], '__dict__'):
                    new_op[key] = depth_copy(op[key])
            return new_op

        ops = self._operations
        new_ops = []
        for op in ops:
            new_ops.append([])
            new_ops[-1].append(op[0])
            new_ops[-1].append(depth_copy(op[1]))

        return new_ops

    @property
    def finalized(self):
        return self._ref_block_num is not None and self._ref_block_prefix is not None\
            and self.chain_id is not None and self.has_all_fees

    @property
    def api(self):
        if not self._api:
            raise Exception('Api instance does not exist, check your connection')
        return self._api

    @api.setter
    def api(self, value):
        if not isinstance(value, Api):
            raise Exception('api is not a Api instance')
        self._api = value

    @property
    def expiration(self):
        if self._expiration:
            return self._expiration

    @expiration.setter
    def expiration(self, value):
        if not isinstance(value, str) or not (len(value.split('-')) == 3):
            raise Exception('expiration is not ISO time format')
        self._expiration = value

    @property
    def has_all_fees(self):
        for op in self._operations:
            if 'fee' not in op[1] or 'amount' not in op[1]['fee']:
                return False
        return True

    def check_not_finalized(self):
        if self.finalized:
            raise Exception('already finalized')

    def check_finalized(self):
        if not self.finalized:
            raise Exception('transaction is not finalized')

    def add_operation(self, name, props):
        self.check_not_finalized()
        if (name is None):
            raise Exception('name is missing')

        if type(name) is str:
            operation_id, operation_class = get_operation_by_name(name)
        else:
            operation_id, operation_class = get_operation_by_id(name)

        if type(operation_id) is not int:
            raise Exception('unknown operation {}'.format(name))

        if not isinstance(props, dict):
            raise Exception('argument "props" is not a dict')

        operation = [operation_id, operation_class(props)]
        self._operations.append(operation)
        return self

    def _get_required_fees(self, operations, asset_id=echo_asset_id):
        return self.api.database.get_required_fees(operations, asset_id)

    def _get_fee_pool(self, asset_id):
        dynamic_asset_data_id = self.api.database.get_objects([asset_id])[0]['dynamic_asset_data_id']
        return self.api.database.get_objects([dynamic_asset_data_id])[0]['fee_pool']

    def set_required_fees(self, asset_id=echo_asset_id):
        self.check_not_finalized()

        if not len(self.operations):
            raise Exception('no operations')

        default_asset_operations = []
        default_asset_indices = []

        non_default_asset_operations = {}
        non_default_asset_indices = {}

        operations_types = self.operations
        assert operations_types == self._operations

        for index, (op_id, op) in enumerate(operations_types):
            op = op.json()
            if 'fee' not in op:
                op.update({'fee': OrderedDict()})
                self._operations[index][1].update({'fee': OrderedDict()})
                self._operations[index][1].move_to_end('fee', last=False)

            if 'asset_id' not in op['fee']:
                op['fee'].update({'asset_id': asset_id})
                self._operations[index][1]['fee'].update({'asset_id': ObjectId(asset_id, 'asset')})
                self._operations[index][1]['fee'].move_to_end('asset_id', last=True)

            if ('asset_id' in op['fee']) and ('amount' in op['fee']):
                continue

            if op['fee']['asset_id'] == echo_asset_id:
                default_asset_indices.append(index)
                default_asset_operations.append([op_id, op])
            else:
                asset_group = op['fee']['asset_id']
                if asset_group not in non_default_asset_operations:
                    non_default_asset_operations.update({asset_group: []})
                    non_default_asset_indices.update({asset_group: []})

                non_default_asset_indices[asset_group].append(index)
                non_default_asset_operations[asset_group].append([op_id, op])

        if len(default_asset_operations):
            fees = self._get_required_fees(default_asset_operations)
            for i, fee in enumerate(fees):
                if isinstance(fee, list):
                    fee = fee[0]
                elif isinstance(fee, dict) and 'fee' in fee:
                    fee = fee['fee']
                self._operations[default_asset_indices[i]][1].update({'fee': Asset(fee)})
                self._operations[default_asset_indices[i]][1].move_to_end('fee', last=False)

        for asset_group in non_default_asset_operations:
            ops = non_default_asset_operations[asset_group]
            fees = self._get_required_fees(ops, asset_group)
            fee_pool = self._get_fee_pool(asset_group)

            total_fees = 0
            for i, fee in enumerate(fees):
                if isinstance(fee, list):
                    fee = fee[0]
                elif isinstance(fee, dict) and 'fee' in fee:
                    fee = fee['fee']
                self._operations[non_default_asset_indices[asset_group][i]][1].update({'fee': Asset(fee)})
                total_fees += fee['amount']

            if total_fees > fee_pool:
                raise Exception('fee pool overflow')

        return self

    def add_signer(self, private):
        private_key = PrivateKey(private)
        private_key_hex = repr(private_key)
        if private_key_hex in self._signers:
            return self

        self._signers.append(private_key_hex)
        return self

    def _get_dynamic_global_chain_data(self, dynamic_global_object_id):
        return self.api.database.get_objects(object_ids=[dynamic_global_object_id])[0]

    def _get_chain_id(self):
        return self.api.database.get_chain_id()

    def set_global_chain_data(self):
        if self.ref_block_num is None or self.ref_block_prefix is None:
            global_chain_data = self._get_dynamic_global_chain_data('2.1.0')
            ref_block_prefix = self.bytes_to_int(
                reversed(bytearray(decode(global_chain_data['head_block_id'], 'hex')[4:8]))
            )
            self.ref_block_num = global_chain_data['head_block_number'] & 0xffff
            self.ref_block_prefix = ref_block_prefix

    def sign(self, _private_key=None):
        if _private_key is not None:
            self.add_signer(_private_key)

        if not self.finalized:
            self.set_global_chain_data()

            if not self.has_all_fees:
                self.set_required_fees()

            if self.chain_id is None:
                self.chain_id = self._get_chain_id()

        if self.expiration is None:

            def seconds_to_iso(sec):
                iso_result = datetime.fromtimestamp(sec, timezone.utc).replace(microsecond=0).isoformat()
                return iso_result[:iso_result.rfind('+')]

            def iso_to_seconds(iso):
                timeformat = "%Y-%m-%dT%H:%M:%S%Z"
                return ceil(timegm(time.strptime((iso + "UTC"), timeformat)))

            now_iso = seconds_to_iso(datetime.now(timezone.utc).timestamp())
            now_seconds = iso_to_seconds(now_iso)
            self.expiration = seconds_to_iso(now_seconds + 300)

        self.check_finalized()

        _transaction = TransactionType(
            ref_block_num=self.ref_block_num,
            ref_block_prefix=self.ref_block_prefix,
            expiration=self.expiration,
            operations=self.operations,
            extensions=[]
        )
        transaction_buffer = bytes(_transaction)
        chain_buffer = bytes.fromhex(self.chain_id)
        self._signatures = list(map(lambda signer: self._crypto.sign_message(chain_buffer + transaction_buffer,
                                    signer).hex(), self._signers))

    @property
    def transaction_object(self):
        self.check_finalized()
        return SignedTransactionType(
            ref_block_num=self.ref_block_num,
            ref_block_prefix=self.ref_block_prefix,
            expiration=self.expiration,
            operations=self.operations,
            extensions=[],
            signatures=self._signatures
        )

    def _get_potential_signatures(self, tr):
        return self.api.database.get_potential_signatures(tr)

    def _get_potential_address_signatures(self, tr):
        return self.api.database.get_potential_address_signatures(tr)

    def get_potential_signatures(self):
        if self.finalized:
            transaction_object = self.transaction_object
        else:
            def change_fee(op):
                op[1].update({'fee': Asset({'amount': 0, 'asset_id': echo_asset_id})})
                op[1].move_to_end('fee', last=False)
                return op
            ops = map(lambda op: change_fee(op), self.operations)

            transaction_object = TransactionType(
                ref_block_num=0,
                ref_block_prefix=0,
                expiration=self.expiration if self.expiration else 0,
                operations=ops,
                extensions=[]
            )

        public_keys = self._get_potential_signatures(transaction_object.json())
        addresses = self._get_potential_address_signatures(transaction_object.json())

        return public_keys, addresses

    def broadcast(self, callback=None):
        if not self.finalized:
            self.sign()
        transaction_object = self.transaction_object
        if callback is None:
            return self.api.network.broadcast_transaction_synchronous(transaction_object.json())
        return self.api.network.broadcast_transaction_with_callback(transaction_object.json(), callback)
