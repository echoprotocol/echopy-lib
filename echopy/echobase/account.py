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

import ecdsa
from iroha import IrohaCrypto


class PasswordKey(Prefix):
    """ It leverages the technology of Brainkeys
        and allows people to have a secure private key by providing a
        passphrase only.
    """

    def __init__(self, account, password, role="active", prefix='ECHO'):
        self.set_prefix(prefix)
        self.account = account
        self.role = role
        self.password = password

    def get_private(self):
        a = _bytes(self.account + self.role + self.password)
        s = hashlib.sha256(a).digest()
        return PrivateKey(hexlify(s).decode("ascii"), prefix=self.prefix)

    def get_public(self):
        return self.get_private().pubkey

    def get_private_key(self):
        return self.get_private()

    def get_public_key(self):
        return self.get_public()


class BrainKey(Prefix):
    """ Given the brain key, a private key is derived as::
            privkey = SHA256(SHA512(brain_key + " " + sequence))

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

    def _normalize(self, brain_key):
        return " ".join(re.compile("[\t\n\v\f\r ]+").split(brain_key))

    def _get_private(self):
        """ Derive private key from the brain key and the current sequence
            number
        """
        encoded = "%s" % (self._brain_key)
        a = _bytes(encoded)
        s = hashlib.sha256(hashlib.sha512(a).digest()).digest()
        return PrivateKey(hexlify(s).decode("ascii"), prefix=self.prefix)



    def get_private_key_base58(self):
        return str(self._get_private())

    def get_private_key_hex(self):
        return repr(self._get_private())

    def get_public_key_base58(self):
        return str(self._get_private().pubkey)

    def get_public_key_hex(self):
        return repr(self._get_private().pubkey)

    def get_echorand_key_base58(self):
        return str(self._get_private().echorand_key)

    def get_echorand_key_hex(self):
        return repr(self._get_private().echorand_key)

    @staticmethod
    def _suggest():
        """ Suggest a new random brain key
        """
        word_count = 16
        brain_key = []
        dict_lines = brain_key_dictionary.split(",")
        assert len(dict_lines) == 2**11
        for _ in range(0, word_count):
            num = int(random.getrandbits(11))
            brain_key.append(dict_lines[num].upper())
        return " ".join(brain_key)



class Address(Prefix):
    """ This class serves as an address representation for Public Keys.
        """

    def __init__(self, address, prefix='ECHO'):
        self.set_prefix(prefix)
        self._address = Base58(address, prefix=self.prefix)

    @classmethod
    def from_pubkey(cls, pubkey, compressed=True, version=56, prefix='ECHO'):
        """ Load an address provided the public key.
        """
        pubkey = PublicKey(pubkey, prefix=prefix or Prefix.prefix)
        if compressed:
            pubkey_plain = pubkey.compressed()
        else:
            pubkey_plain = pubkey.uncompressed()
        sha = hashlib.sha256(unhexlify(pubkey_plain)).hexdigest()
        rep = hexlify(ripemd160(sha)).decode("ascii")
        s = ("%.2x" % version) + rep
        result = s + hexlify(doublesha256(s)[:4]).decode("ascii")
        result = hexlify(ripemd160(result)).decode("ascii")
        return cls(result, prefix=pubkey.prefix)

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
    def from_pubkey(cls, pubkey, compressed=True, version=56, prefix='ECHO'):
        pubkey = PublicKey(pubkey, prefix=prefix or Prefix.prefix)
        if compressed:
            pubkey_plain = pubkey.compressed()
        else:
            pubkey_plain = pubkey.uncompressed()

        addressbin = ripemd160(hashlib.sha512(unhexlify(pubkey_plain)).hexdigest())
        result = Base58(hexlify(addressbin).decode("ascii"))
        return cls(result, prefix=pubkey.prefix)


class PublicKey(Prefix):
    """ This class deals with Public Keys and inherits ``Address``.
    """

    def __init__(self, pk, prefix='ECHO'):
        self.set_prefix(prefix)
        if isinstance(pk, PublicKey):
            pk = format(pk, self.prefix)

        if str(pk).startswith("04"):
            order = ecdsa.SECP256k1.order
            p = ecdsa.VerifyingKey.from_string(
                unhexlify(pk[2:]), curve=ecdsa.SECP256k1
            ).pubkey.point
            x_str = ecdsa.util.number_to_string(p.x(), order)
            pk = hexlify(chr(2 + (p.y() & 1)).encode("ascii") + x_str).decode("ascii")

        self._pk = Base58(pk, prefix=self.prefix)

    @property
    def pubkey(self):
        return self._pk

    @property
    def compressed_key(self):
        return PublicKey(self.compressed())

    def _derive_y_from_x(self, x, is_even):
        """ Derive y point from x point """
        curve = ecdsa.SECP256k1.curve
        # The curve equation over F_p is:
        #   y^2 = x^3 + ax + b
        a, b, p = curve.a(), curve.b(), curve.p()
        alpha = (pow(x, 3, p) + a * x + b) % p
        beta = ecdsa.numbertheory.square_root_mod_prime(alpha, p)
        if (beta % 2) == is_even:
            beta = p - beta
        return beta

    def compressed(self):
        """ returns the compressed key """
        return repr(self._pk)

    def uncompressed(self):
        """ Derive uncompressed key """
        public_key = repr(self._pk)
        prefix = public_key[0:2]
        assert prefix == "02" or prefix == "03"
        x = int(public_key[2:], 16)
        y = self._derive_y_from_x(x, (prefix == "02"))
        key = "04" + "%064x" % x + "%064x" % y
        return key

    def point(self):
        string = unhexlify(self.unCompressed())
        return ecdsa.VerifyingKey.from_string(
            string[1:], curve=ecdsa.SECP256k1
        ).pubkey.point

    def child(self, offset256):
        """ Derive new public key from this key and a sha256 "offset" """
        a = bytes(self) + offset256
        s = hashlib.sha256(a).digest()
        return self.add(s)

    def add(self, digest256):
        """ Derive new public key from this key and a sha256 "digest" """
        from .ecdsa import tweakaddPubkey

        return tweakaddPubkey(self, digest256)

    @classmethod
    def from_privkey(cls, privkey, prefix='ECHO'):
        """ Derive uncompressed public key """
        privkey = PrivateKey(privkey, prefix=prefix or Prefix.prefix)
        secret = unhexlify(repr(privkey))
        order = ecdsa.SigningKey.from_string(
            secret, curve=ecdsa.SECP256k1
        ).curve.generator.order()
        p = ecdsa.SigningKey.from_string(
            secret, curve=ecdsa.SECP256k1
        ).verifying_key.pubkey.point
        x_str = ecdsa.util.number_to_string(p.x(), order)
        compressed = hexlify(chr(2 + (p.y() & 1)).encode("ascii") + x_str).decode(
            "ascii"
        )
        return cls(compressed, prefix=prefix or Prefix.prefix)

    def __repr__(self):
        """ Gives the hex representation of the ECHO public key. """
        return repr(self._pk)

    def __str__(self):
        """ Returns the readable ECHO public key
        """
        return format(self._pk, self.prefix)

    def __format__(self, _format):
        return format(self._pk, _format)

    def __bytes__(self):
        return bytes(self._pk)

    def __lt__(self, other):
        assert isinstance(other, PublicKey)
        return repr(self.address) < repr(other.address)

    def unCompressed(self):
        return self.uncompressed()

    @property
    def address(self):
        return EchoAddress.from_pubkey(repr(self), prefix=self.prefix)


class PrivateKey(Prefix):
    """ Derives the compressed and uncompressed public keys and
        constructs two instances of ``PublicKey``
    """

    def __init__(self, wif=None, prefix='ECHO'):
        self.set_prefix(prefix)
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
        return Address.from_pubkey(self.pubkey, prefix=self.prefix)

    @property
    def pubkey(self):
        return self.compressed

    @property
    def compressed(self):
        return PublicKey.from_privkey(self, prefix=self.prefix)

    @property
    def uncompressed(self):
        return PublicKey(self.pubkey.uncompressed(), prefix=self.prefix)

    def get_secret(self):
        """ Get sha256 digest of the wif key.
        """
        return hashlib.sha256(bytes(self)).digest()

    def derive_private_key(self, sequence):
        encoded = "%s %d" % (str(self), sequence)
        a = bytes(encoded, "ascii")
        s = hashlib.sha256(hashlib.sha512(a).digest()).digest()
        return PrivateKey(hexlify(s).decode("ascii"), prefix=self.pubkey.prefix)

    def child(self, offset256):
        """ Derive new private key from this key and a sha256 "offset"
        """
        a = bytes(self.pubkey) + offset256
        s = hashlib.sha256(a).digest()
        return self.derive_from_seed(s)

    def derive_from_seed(self, offset):
        seed = int(hexlify(bytes(self)).decode("ascii"), 16)
        z = int(hexlify(offset).decode("ascii"), 16)
        order = ecdsa.SECP256k1.order
        secexp = (seed + z) % order
        secret = "%0x" % secexp
        return PrivateKey(secret, prefix=self.pubkey.prefix)

    @property
    def echorand_key(self):
        return EchorandKey(wif=self._wif)

    def __format__(self, _format):
        return format(self._wif, _format)

    def __repr__(self):
        """ Hex representation of the private key."""
        return repr(self._wif)

    def __str__(self):
        """ Returns the readable ECHO private key.
        """
        return format(self._wif, "WIF")

    def __bytes__(self):
        """ Returns the raw private key """
        return bytes(self._wif)


class EchorandKey(Prefix):

    def __init__(self, wif, prefix='DET'):
        self.set_prefix(prefix)
        self.crypto = IrohaCrypto()
        self._echorand_key = Base58(self.crypto.derive_public_key(repr(wif)).decode())

    def __repr__(self):
        """ Gives the hex representation of the ECHO echorand key.
        """
        return repr(self._echorand_key)

    def __str__(self):
        """ Returns the readable ECHO echorand key.
        """
        return format(self._echorand_key, self.prefix)

    def __format__(self, _format):
        return format(self._echorand_key, _format)

    def __bytes__(self):
        return bytes(self._echorand_key)
