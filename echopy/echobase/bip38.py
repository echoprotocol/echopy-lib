# -*- coding: utf-8 -*-
import logging
import hashlib
from binascii import hexlify, unhexlify
from .account import PrivateKey
from .base58 import Base58, base58decode
from .utils import _bytes

log = logging.getLogger(__name__)

try:
    from Cryptodome.Cipher import AES
except ImportError:
    try:
        from Crypto.Cipher import AES
    except ImportError:
        raise ImportError("Missing dependency: pyCryptodome")

SCRYPT_MODULE = None
if not SCRYPT_MODULE:
    try:
        import scrypt

        SCRYPT_MODULE = "scrypt"
    except ImportError:
        try:
            import pylibscrypt as scrypt

            SCRYPT_MODULE = "pylibscrypt"
        except ImportError:
            raise ImportError("Missing dependency: scrypt or pylibscrypt")

log.debug("Using scrypt module: %s" % SCRYPT_MODULE)


class SaltException(Exception):
    pass


def _encrypt_xor(a, b, aes):
    a = unhexlify("%0.32x" % (int((a), 16) ^ int(hexlify(b), 16)))
    return aes.encrypt(a)


def encrypt(privkey, passphrase):
    """ BIP0038 non-ec-multiply encryption. Returns BIP0038 encrypted private key.
    """
    if isinstance(privkey, str):
        privkey = PrivateKey(privkey)
    else:
        privkey = PrivateKey(repr(privkey))

    privkeyhex = repr(privkey)
    addr = format(privkey.bitcoin.address, "ECHO")
    a = _bytes(addr)
    salt = hashlib.sha256(hashlib.sha256(a).digest()).digest()[0:4]
    if SCRYPT_MODULE == "scrypt":  # pragma: no cover
        key = scrypt.hash(passphrase, salt, 16384, 8, 8)
    elif SCRYPT_MODULE == "pylibscrypt":  # pragma: no cover
        key = scrypt.scrypt(bytes(passphrase, "utf-8"), salt, 16384, 8, 8)
    else:  # pragma: no cover
        raise ValueError("No scrypt module loaded")  # pragma: no cover
    (derived_half1, derived_half2) = (key[:32], key[32:])
    aes = AES.new(derived_half2, AES.MODE_ECB)
    encrypted_half1 = _encrypt_xor(privkeyhex[:32], derived_half1[:16], aes)
    encrypted_half2 = _encrypt_xor(privkeyhex[32:], derived_half1[16:], aes)
    " flag byte is forced 0xc0 because Echo only uses compressed keys "
    payload = b"\x01" + b"\x42" + b"\xc0" + salt + encrypted_half1 + encrypted_half2
    " Checksum "
    checksum = hashlib.sha256(hashlib.sha256(payload).digest()).digest()[:4]
    privatkey = hexlify(payload + checksum).decode("ascii")
    return Base58(privatkey)


def decrypt(encrypted_privkey, passphrase):
    """BIP0038 non-ec-multiply decryption. Returns WIF private key.
    """

    d = unhexlify(base58decode(encrypted_privkey))
    d = d[2:]
    flagbyte = d[0:1]
    d = d[1:]
    assert flagbyte == b"\xc0", "Flagbyte has to be 0xc0"
    salt = d[0:4]
    d = d[4:-4]
    if SCRYPT_MODULE == "scrypt":
        key = scrypt.hash(passphrase, salt, 16384, 8, 8)
    elif SCRYPT_MODULE == "pylibscrypt":
        key = scrypt.scrypt(bytes(passphrase, "utf-8"), salt, 16384, 8, 8)
    else:
        raise ValueError("No scrypt module loaded")
    derivedhalf1 = key[0:32]
    derivedhalf2 = key[32:64]
    encryptedhalf1 = d[0:16]
    encryptedhalf2 = d[16:32]
    aes = AES.new(derivedhalf2, AES.MODE_ECB)
    decryptedhalf2 = aes.decrypt(encryptedhalf2)
    decryptedhalf1 = aes.decrypt(encryptedhalf1)
    privraw = decryptedhalf1 + decryptedhalf2
    privraw = "%064x" % (int(hexlify(privraw), 16) ^ int(hexlify(derivedhalf1), 16))
    wif = Base58(privraw)
    privkey = PrivateKey(format(wif, "wif"))
    addr = format(privkey.bitcoin.address, "BTC")
    a = _bytes(addr)
    saltverify = hashlib.sha256(hashlib.sha256(a).digest()).digest()[0:4]
    if saltverify != salt:
        raise SaltException("checksum verification failed! Password may be incorrect.")
    return wif
