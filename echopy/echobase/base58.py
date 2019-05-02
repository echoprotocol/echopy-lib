# -*- coding: utf-8 -*-
import hashlib
import string
import logging

from binascii import hexlify, unhexlify
from .utils import _bytes
from .prefix import Prefix

log = logging.getLogger(__name__)


class Base58(Prefix):
    """Base58 base class

    This class serves as an abstraction layer to deal with base58 encoded
    strings and their corresponding hex and binary representation throughout
    the library.
    """

    def __init__(self, data, prefix=None):
        self.set_prefix(prefix)
        if isinstance(data, Base58):
            data = repr(data)
        if all(c in string.hexdigits for c in data):
            self._hex = data
        else:
            if self.prefix is not None and data[: len(self.prefix)] == self.prefix:
                data = data[len(self.prefix):]
            self._hex = base58decode(data)

    def __format__(self, _format):
        return str(self) if _format == 'WIF' else _format.upper() + str(self)

    def __repr__(self):
        return self._hex

    def __str__(self):
        return base58encode(self._hex)

    def __bytes__(self):
        return unhexlify(self._hex)


# https://github.com/tochev/python3-cryptocoins/raw/master/cryptocoins/base58.py
BASE58_ALPHABET = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def base58decode(base58_str):
    base58_text = _bytes(base58_str)
    n = 0
    leading_zeroes_count = 0
    for b in base58_text:
        n = n * 58 + BASE58_ALPHABET.find(b)
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 256:
        div, mod = divmod(n, 256)
        res.insert(0, mod)
        n = div
    else:
        res.insert(0, n)
    return hexlify(bytearray(1) * leading_zeroes_count + res).decode("ascii")


def base58encode(hexstring):
    byteseq = unhexlify(_bytes(hexstring))
    n = 0
    leading_zeroes_count = 0
    for c in byteseq:
        n = n * 256 + c
        if n == 0:
            leading_zeroes_count += 1
    res = bytearray()
    while n >= 58:
        div, mod = divmod(n, 58)
        res.insert(0, BASE58_ALPHABET[mod])
        n = div
    else:
        res.insert(0, BASE58_ALPHABET[n])
    return (BASE58_ALPHABET[0:1] * leading_zeroes_count + res).decode("ascii")


def ripemd160(s):
    ripemd160 = hashlib.new("ripemd160")
    ripemd160.update(unhexlify(s))
    return ripemd160.digest()


def doublesha256(s):
    return hashlib.sha256(hashlib.sha256(unhexlify(s)).digest()).digest()


def b58encode(v):
    return base58encode(v)


def b58decode(v):
    return base58decode(v)
