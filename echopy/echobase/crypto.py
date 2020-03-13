import hashlib
import binascii
from iroha import ed25519


class Crypto:

    @staticmethod
    def derive_public_key(private_key):
        """
        Calculate public key from private key.

        :param private_key: hex encoded private key
        :return: hex encoded public key
        """
        secret = binascii.unhexlify(private_key)
        public_key = ed25519.publickey_unsafe(secret)
        hex_public_key = binascii.hexlify(public_key)
        return hex_public_key

    @staticmethod
    def hash(message):
        return hashlib.sha256(message).digest()

    @staticmethod
    def sign_message(message, private_key):
        """
        Calculate signature for given message and private key.

        :param message: proto that has payload message inside
        :param private_key: hex string with private key
        :return: signature bytes string
        """
        public_key = Crypto.derive_public_key(private_key).decode()
        sk = binascii.unhexlify(private_key)
        pk = binascii.unhexlify(public_key)
        message_hash = Crypto.hash(message)
        signature_bytes = ed25519.signature_unsafe(message_hash, sk, pk)
        return signature_bytes
