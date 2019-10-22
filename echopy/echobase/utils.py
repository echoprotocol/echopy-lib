# -*- coding: utf-8 -*-
import sys
import time
import struct
from hashlib import sha256
from datetime import datetime, timezone

timeFormat = "%Y-%m-%dT%H:%M:%S"


def _bytes(x):
    if sys.version > "3":
        return bytes(x, "utf8")
    else:
        return x.__bytes__()


def unicodify(data):
    r = []
    for s in data:
        o = ord(s)
        if (o <= 7) or (o == 11) or (o > 13 and o < 32):
            r.append("u%04x" % o)
        elif o == 8:
            r.append("b")
        elif o == 9:
            r.append("\t")
        elif o == 10:
            r.append("\n")
        elif o == 12:
            r.append("f")
        elif o == 13:
            r.append("\r")
        else:
            r.append(s)
    return bytes("".join(r), "utf-8")


def format_time(t):
    """Properly Format Time for permlinks."""
    if isinstance(t, (float, int)):
        return datetime.utcfromtimestamp(t).strftime(timeFormat)
    elif isinstance(t, datetime):
        return t.strftime(timeFormat)
    else:
        raise ValueError("formatTime expects float/int, or datetime")


def format_time_from_now(secs=0):
    """Properly Format Time that is `x` seconds in the future."""
    return datetime.utcfromtimestamp(time.time() + int(secs)).strftime(timeFormat)


def parse_time(block_time):
    """Take a string representation of time from the blockchain, and parse it into datetime object."""
    return datetime.strptime(block_time, timeFormat).replace(tzinfo=timezone.utc)


def solve_registration_task(block_id, rand_num, difficulty):

    bytebuffer = bytes.fromhex(block_id) + struct.pack("<Q", int(rand_num))
    iterator = 0
    while True:
        bytebuffer_to_hash = bytebuffer + struct.pack("<Q", iterator)
        calculated_hash = sha256(bytebuffer_to_hash)
        solution_power = 0
        for byte in calculated_hash.digest():
            if byte == 0:
                solution_power += 8
                continue
            divider = 1 << 7
            while byte < divider:
                solution_power += 1
                divider >>= 1
            break

        if solution_power > difficulty:
            return iterator

        iterator += 1

formatTimeString = format_time
