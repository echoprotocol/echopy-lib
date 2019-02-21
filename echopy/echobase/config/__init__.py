from .api_config import ApiConfig
from .chain_config import ChainConfig
from .chain_types import ChainTypes
from .object_types import ObjectTypes
from .operations_ids import OperationIds
from .ws_constants import WSConfig


class Config:
    def __init__(self):
        self.api = ApiConfig()
        self.chain = ChainConfig()
        self.chain_types = ChainTypes()
        self.object_types = ObjectTypes()
        self.operation_ids = OperationIds()
        self.ws = WSConfig()
        self.start_operation_id = '1.11.0'
        self.core_asset_id = '1.3.0'
        self.echorand_types = {
            'START_NOTIFICATION': 1,
            'BLOCK_NOTIFICATION': 2
        }
        self.cancel_limit_order = 'cancel-limit-order'
        self.update_call_order = 'update_call_order'
        self.close_call_order = 'close-call-order'
        self.bitasset_update = 'bitasset-update'
        self.echo_asset_id = '1.3.0'
        self.dynamic_global_object_id = '2.1.0'


__all__ = [
    "api_config",
    "chain_config",
    "chain_types",
    "object_types",
    "operations_ids",
    "ws_constants"
]