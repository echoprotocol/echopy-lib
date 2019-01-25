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
from .signedtransactions import Signed_Transaction
from .objects import GrapheneObject, isArgsThisClass, Operation

timeformat = "%Y-%m-%dT%H:%M:%S%Z"


def getBlockParams(ws):
    """ Auxiliary method to obtain ``ref_block_num`` and
        ``ref_block_prefix``. Requires a websocket connection to a
        witness node!
    """
    dynBCParams = ws.get_dynamic_global_properties()
    ref_block_num = dynBCParams["head_block_number"] & 0xFFFF
    ref_block_prefix = struct.unpack_from(
        "<I", unhexlify(dynBCParams["head_block_id"]), 4
    )[0]
    return ref_block_num, ref_block_prefix


def formatTimeFromNow(secs=0):
    """ Properly Format Time that is `x` seconds in the future

     :param int secs: Seconds to go in the future (`x>0`) or the past (`x<0`)
     :return: Properly formated time for Graphene (`%Y-%m-%dT%H:%M:%S`)
     :rtype: str

    """
    return datetime.utcfromtimestamp(time.time() + int(secs)).strftime(timeformat)
