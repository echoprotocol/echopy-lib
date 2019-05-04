from .api_config import ApiConfig
from .chain_config import ChainConfig
from .implementation_object_types import ImplementationObjectTypes
from .object_types import ObjectTypes
from .operations_ids import OperationIds
from .reserved_spaces import ReservedSpaces
from .ws_constants import WSConfig


class Config:
    def __init__(self):
        self.api = ApiConfig()
        self.chain = ChainConfig()
        self.implementation_object_types = ImplementationObjectTypes()
        self.object_types = ObjectTypes()
        self.operation_ids = OperationIds()
        self.reserved_spaces = ReservedSpaces()
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
    "implementation_object_types",
    "object_types",
    "operations_ids",
    "reserved_spaces",
    "ws_constants"
]