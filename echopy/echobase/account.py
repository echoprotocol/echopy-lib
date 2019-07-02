# -*- coding: utf-8 -*-
from __future__ import absolute_import

import hashlib
import re
import random

from binascii import hexlify, unhexlify
from .base58 import ripemd160, Base58, doublesha256
from .bip39_dictionary import words as brain_key_dictionary
from .utils import _bytes
from .prefix import Prefix
from .crypto import Crypto


class BrainKey(Prefix):
    """ Given the brain key, a private key is derived as::
            private_key = SHA256(SHA512(brain_key))

        Incrementing the sequence number yields a new key that can be
        regenerated given the brain key.

    """

    def __init__(self, brain_key=None, prefix='ECHO'):
        self.set_prefix(prefix)
        if not brain_key:
            self._brain_key = BrainKey._suggest()
        else:
            self._brain_key = self._normalize(brain_key).strip()

    def __next__(self):
        """ Get the next private key for iterators
        """
        return self.next_brain_key()

    @property
    def brain_key(self):
        return self._normalize(self._brain_key)

    @brain_key.setter
    def brain_key(self, brain_key):
        assert isinstance(brain_key, (str, list))
        if isinstance(brain_key, list):
            assert len(brain_key) == 16
            for word in brain_key:
                assert isinstance(word, str)
            brain_key = ' '.join(brain_key).upper()
        else:
            separator = ' ' if brain_key.find(',') < 0 else ','
            words = brain_key.split(separator)
            assert len(words) == 16
            brain_key = ' '.join(words).upper()
        self._brain_key = brain_key

    def next_brain_key(self):
        self._brain_key = self._suggest()
        return self

    @staticmethod
    def _suggest():
        """ Suggest a new random brain key.
        """
        word_count = 16
        brain_key = []
        dict_lines = brain_key_dictionary.split(",")
        assert len(dict_lines) == 2**11
        for _ in range(0, word_count):
            num = int(random.getrandbits(11))
            brain_key.append(dict_lines[num].upper())
        return " ".join(brain_key)

    def _normalize(self, brain_key):
        return " ".join(re.compile("[\t\n\v\f\r ]+").split(brain_key))

    def _get_private(self):
        encoded = "%s" % (self._brain_key)
        a = _bytes(encoded)
        s = hashlib.sha256(hashlib.sha512(a).digest()).digest()
        return PrivateKey(hexlify(s).decode("ascii"))

    def get_private_key_base58(self):
        return str(self._get_private())

    def get_private_key_hex(self):
        return repr(self._get_private())

    def get_public_key_base58(self):
        return str(self._get_private().public_key)

    def get_public_key_hex(self):
        return repr(self._get_private().public_key)


class Address(Prefix):
    """ This class serves as an address representation for Public Keys.
        """

    def __init__(self, address, prefix='ECHO'):
        self.set_prefix(prefix)
        self._address = Base58(address, prefix=self.prefix)

    @classmethod
    def from_public_key(cls, public_key, version=56, prefix='ECHO'):
        """ Load an address provided the public key.
        """
        public_key = PublicKey(public_key, prefix=prefix or Prefix.prefix)
        public_key_plain = repr(public_key)
        sha = hashlib.sha256(unhexlify(public_key_plain)).hexdigest()
        rep = hexlify(ripemd160(sha)).decode("ascii")
        s = ("%.2x" % version) + rep
        result = s + hexlify(doublesha256(s)[:4]).decode("ascii")
        result = hexlify(ripemd160(result)).decode("ascii")
        return cls(result, prefix=public_key.prefix)

    def __repr__(self):
        """ Gives the hex representation of the ECHO address
        """
        return repr(self._address)

    def __str__(self):
        """ Returns the readable ECHO address.
        """
        return format(self._address, self.prefix)

    def __format__(self, _format):
        return format(self._address, _format)

    def __bytes__(self):
        return bytes(self._address)


class EchoAddress(Address):

    @classmethod
    def from_public_key(cls, public_key, version=56, prefix='ECHO'):
        if not isinstance(public_key, PublicKey):
            public_key = PublicKey(public_key, prefix=prefix or Prefix.prefix)
        public_key_plain = repr(public_key)

        address_bin = ripemd160(hashlib.sha512(unhexlify(public_key_plain)).hexdigest())
        result = Base58(hexlify(address_bin).decode("ascii"))
        return cls(result, prefix=public_key.prefix)


class PrivateKey(Prefix):
    """ Derives the compressed and uncompressed public keys and
        constructs two instances of ``PublicKey``
    """

    def __init__(self, wif=None):
        if wif is None:
            import os
            self._wif = Base58(hexlify(os.urandom(32)).decode("ascii"))
        elif isinstance(wif, PrivateKey):
            self._wif = wif._wif
        elif isinstance(wif, Base58):
            self._wif = wif
        else:
            self._wif = Base58(wif)

        assert len(repr(self._wif)) == 64

    @property
    def address(self):
        return self.public_key.address

    def get_secret(self):
        """ Get sha256 digest of the wif key.
        """
        return hashlib.sha256(bytes(self)).digest()

    @property
    def public_key(self):
        return PublicKey.from_private_key(self._wif)

    def __format__(self, _format):
        return format(self._wif, _format)

    def __repr__(self):
        """ Hex representation of the private key."""
        return repr(self._wif)

    def __str__(self):
        """ Returns the readable ECHO private key.
        """
        return format(self._wif, 'WIF')

    def __bytes__(self):
        """ Returns the raw private key """
        return bytes(self._wif)


class PublicKey(Prefix):

    def __init__(self, public_key, prefix='ECHO'):
        self.set_prefix(prefix)
        self._public_key = Base58(public_key, prefix=self.prefix)

    @classmethod
    def from_private_key(cls, private_key):
        private_key = PrivateKey(private_key)
        public_key = Crypto.derive_public_key(repr(private_key)).decode()
        return cls(public_key)

    def __repr__(self):
        """ Gives the hex representation of the ECHO echorand key.
        """
        return repr(self._public_key)

    def __str__(self):
        """ Returns the readable ECHO echorand key.
        """
        return format(self._public_key, self.prefix)

    def __format__(self, _format):
        return format(self._public_key, _format)

    def __bytes__(self):
        return bytes(self._public_key)

    @property
    def address(self):
        return EchoAddress.from_public_key(self, prefix=self.prefix)
