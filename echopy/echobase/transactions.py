# -*- coding: utf-8 -*-
import json
import struct
import time

from collections import OrderedDict
from binascii import hexlify, unhexlify
from calendar import timegm
from datetime import datetime

from .account import PublicKey
from .chains import known_chains
from .objects import EchoObject, isArgsThisClass, Operation

timeformat = "%Y-%m-%dT%H:%M:%S%Z"


def get_block_params(ws):
    dynBCParams = ws.get_dynamic_global_properties()
    ref_block_num = dynBCParams["head_block_number"] & 0xFFFF
    ref_block_prefix = struct.unpack_from(
        "<I", unhexlify(dynBCParams["head_block_id"]), 4
    )[0]
    return ref_block_num, ref_block_prefix


def format_time_from_now(secs=0):
    return datetime.utcfromtimestamp(time.time() + int(secs)).strftime(timeformat)
