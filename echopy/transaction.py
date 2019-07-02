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
                ("operations", Array([StaticVariant(op, op_id) for op_id, op in kwargs['operations']])),
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
                ("operations", Array([StaticVariant(op, op_id) for op_id, op in kwargs['operations']])),
                ("extensions", Set([])),
                ("signatures", Array([Bytes(signature) for signature in kwargs['signatures']])),
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
        self._crypto = Crypto

    @property
    def ref_block_num(self):
        self.check_finalized()
        return self._ref_block_num

    @property
    def ref_block_prefix(self):
        self.check_finalized()
        return self._ref_block_prefix

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
        return self._finalized

    @property
    def api(self):
        return self._api

    @api.setter
    def api(self, value):
        if not isinstance(value, Api):
            raise Exception('value is not a Api instance')
        self._api = value

    @property
    def expiration(self):
        if self._expiration:
            return copy(self._expiration)

    @expiration.setter
    def expiration(self, value):
        if (type(value) is not str) or not (len(value.split('-')) == 3):
            raise Exception('expiration is not ISO time format')
        self._expiration = value

    @property
    def has_all_fees(self):
        for op in self._operations:
            if 'fee' not in op or 'amount' not in op['fee']:
                return False
        return True

    def check_not_finalized(self):
        if self.finalized:
            raise Exception('already finalized')

    def check_finalized(self):
        if not self.finalized:
            raise Exception('transaction is not finalized')

    def add_operation(self, name, props: dict):
        self.check_not_finalized()
        if (name is None):
            raise Exception('name is missing')

        if type(name) is str:
            operation_id, operation_class = get_operation_by_name(name)
        else:
            operation_id, operation_class = get_operation_by_id(name)

        if type(operation_id) is not int:
            raise Exception('unknown operation {}'.format(name))

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

            if op['fee']['asset_id'] == '1.3.0':
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
                if 'fee' in fee:
                    fee = fee['fee']
                self._operations[default_asset_indices[i]][1].update({'fee': Asset(fee)})
                self._operations[default_asset_indices[i]][1].move_to_end('fee', last=False)

        for asset_group in non_default_asset_operations:
            ops = non_default_asset_operations[asset_group]
            fees = self._get_required_fees(ops, asset_group)
            fee_pool = self._get_fee_pool(asset_group)

            total_fees = 0
            for i, fee in enumerate(fees):
                if 'fee' in fee:
                    fee = fee['fee']
                self._operations[non_default_asset_indices[asset_group][i]][1].update({'fee': Asset(fee)})
                total_fees += fee['amount']

            if total_fees > fee_pool:
                raise Exception('fee pool overflow')

        return self

    def add_signer(self, private):
        self.check_not_finalized()
        private_key = PrivateKey(private)
        private_key_hex = repr(private_key)
        if private_key_hex in self._signers:
            return self

        self._signers.append(private_key_hex)
        return self

    def _get_dynamic_global_chain_data(self, dynamic_global_object_id):
        return self.api.database.get_objects(object_ids=[dynamic_global_object_id])

    def _get_chain_id(self):
        return self.api.database.get_chain_id()

    def sign(self, _private_key=None):
        self.check_not_finalized()
        if _private_key is not None:
            self.add_signer(_private_key)

        if not self.has_all_fees:
            self.set_required_fees()

        dynamic_global_chain_data = self._get_dynamic_global_chain_data(dynamic_global_object_id='2.1.0')[0]

        chain_id = self._get_chain_id()

        self.check_not_finalized()
        self._finalized = True

        self._ref_block_num = dynamic_global_chain_data['head_block_number'] & 0xffff

        def bytes_to_int(bytes):
            result = 0
            for b in bytes:
                result = result * 256 + int(b)
            return result

        little_endian = bytearray(decode(dynamic_global_chain_data['head_block_id'], 'hex')[4:8])
        little_endian.reverse()
        self._ref_block_prefix = bytes_to_int(little_endian)

        if self.expiration is None:

            def seconds_to_iso(sec):
                iso_result = datetime.fromtimestamp(sec, timezone.utc).replace(microsecond=0).isoformat()
                return iso_result[:iso_result.rfind('+')]

            def iso_to_seconds(iso):
                timeformat = "%Y-%m-%dT%H:%M:%S%Z"
                return ceil(timegm(time.strptime((iso + "UTC"), timeformat)))

            head_block_time_iso = dynamic_global_chain_data['time']
            head_block_time_seconds = iso_to_seconds(head_block_time_iso)
            now_iso = seconds_to_iso(datetime.now(timezone.utc).timestamp())
            now_seconds = iso_to_seconds(now_iso)
            expired = now_seconds - head_block_time_seconds > 30
            self.expiration = seconds_to_iso(head_block_time_seconds + 3) if expired\
                else (seconds_to_iso(now_seconds + 3) if now_seconds > head_block_time_seconds
                      else seconds_to_iso(head_block_time_seconds + 3))

        _transaction = TransactionType(
            ref_block_num=self.ref_block_num,
            ref_block_prefix=self.ref_block_prefix,
            expiration=self.expiration,
            operations=self.operations,
            extensions=[]
        )
        transaction_buffer = bytes(_transaction)
        chain_buffer = bytes.fromhex(chain_id)
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
