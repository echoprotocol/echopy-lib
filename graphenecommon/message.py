# -*- coding: utf-8 -*-
import json
import logging
import re

from binascii import hexlify, unhexlify

from graphenebase.ecdsa import sign_message, verify_message

from .exceptions import (
    AccountDoesNotExistsException,
    InvalidMemoKeyException,
    InvalidMessageSignature,
    WrongMemoKey,
)
from .instance import AbstractBlockchainInstanceProvider


log = logging.getLogger(__name__)


class Message(AbstractBlockchainInstanceProvider):
    """ Allow to sign and verify Messages that are sigend with a private key
    """

    MESSAGE_SPLIT = (
        "-----BEGIN GRAPHENE SIGNED MESSAGE-----",
        "-----BEGIN META-----",
        "-----BEGIN SIGNATURE-----",
        "-----END GRAPHENE SIGNED MESSAGE-----",
    )

    # This is the message that is actually signed
    SIGNED_MESSAGE_META = """{message}
account={meta[account]}
memokey={meta[memokey]}
block={meta[block]}
timestamp={meta[timestamp]}"""

    SIGNED_MESSAGE_ENCAPSULATED = """
{MESSAGE_SPLIT[0]}
{message}
{MESSAGE_SPLIT[1]}
account={meta[account]}
memokey={meta[memokey]}
block={meta[block]}
timestamp={meta[timestamp]}
{MESSAGE_SPLIT[2]}
{signature}
{MESSAGE_SPLIT[3]}"""

    def __init__(self, message, *args, **kwargs):
        self.define_classes()
        assert self.account_class
        assert self.publickey_class

        self.message = message.replace("\r\n", "\n")
        self.signed_by_account = None
        self.signed_by_name = None
        self.meta = None
        self.plain_message = None

    def sign(self, account=None, **kwargs):
        """ Sign a message with an account's memo key

            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)
            :raises ValueError: If not account for signing is provided

            :returns: the signed message encapsulated in a known format
        """
        if not account:
            if "default_account" in self.blockchain.config:
                account = self.blockchain.config["default_account"]
        if not account:
            raise ValueError("You need to provide an account")

        # Data for message
        account = self.account_class(account, blockchain_instance=self.blockchain)
        info = self.blockchain.info()
        meta = dict(
            timestamp=info["time"],
            block=info["head_block_number"],
            memokey=account["options"]["memo_key"],
            account=account["name"],
        )

        # wif key
        wif = self.blockchain.wallet.getPrivateKeyForPublicKey(
            account["options"]["memo_key"]
        )

        # We strip the message here so we know for sure there are no trailing
        # whitespaces or returns
        message = self.message.strip()

        enc_message = self.SIGNED_MESSAGE_META.format(**locals())

        # signature
        signature = hexlify(sign_message(enc_message, wif)).decode("ascii")

        self.signed_by_account = account
        self.signed_by_name = account["name"]
        self.meta = meta
        self.plain_message = message

        return self.SIGNED_MESSAGE_ENCAPSULATED.format(
            MESSAGE_SPLIT=self.MESSAGE_SPLIT, **locals()
        )

    def verify(self, **kwargs):
        """ Verify a message with an account's memo key

            :param str account: (optional) the account that owns the bet
                (defaults to ``default_account``)

            :returns: True if the message is verified successfully
            :raises InvalidMessageSignature if the signature is not ok
        """
        # Split message into its parts
        parts = re.split("|".join(self.MESSAGE_SPLIT), self.message)
        parts = [x for x in parts if x.strip()]

        assert len(parts) > 2, "Incorrect number of message parts"

        # Strip away all whitespaces before and after the message
        message = parts[0].strip()
        signature = parts[2].strip()
        # Parse the meta data
        meta = dict(re.findall(r"(\S+)=(.*)", parts[1]))

        log.info("Message is: {}".format(message))
        log.info("Meta is: {}".format(json.dumps(meta)))
        log.info("Signature is: {}".format(signature))

        # Ensure we have all the data in meta
        assert "account" in meta, "No 'account' could be found in meta data"
        assert "memokey" in meta, "No 'memokey' could be found in meta data"
        assert "block" in meta, "No 'block' could be found in meta data"
        assert "timestamp" in meta, "No 'timestamp' could be found in meta data"

        account_name = meta.get("account").strip()
        memo_key = meta["memokey"].strip()

        try:
            self.publickey_class(memo_key, prefix=self.blockchain.prefix)
        except Exception:
            raise InvalidMemoKeyException("The memo key in the message is invalid")

        # Load account from blockchain
        try:
            account = self.account_class(
                account_name, blockchain_instance=self.blockchain
            )
        except AccountDoesNotExistsException:
            raise AccountDoesNotExistsException(
                "Could not find account {}. Are you connected to the right chain?".format(
                    account_name
                )
            )

        # Test if memo key is the same as on the blockchain
        if not account["options"]["memo_key"] == memo_key:
            raise WrongMemoKey(
                "Memo Key of account {} on the Blockchain ".format(account["name"])
                + "differs from memo key in the message: {} != {}".format(
                    account["options"]["memo_key"], memo_key
                )
            )

        # Reformat message
        enc_message = self.SIGNED_MESSAGE_META.format(**locals())

        # Verify Signature
        pubkey = verify_message(enc_message, unhexlify(signature))

        # Verify pubky
        pk = self.publickey_class(
            hexlify(pubkey).decode("ascii"), prefix=self.blockchain.prefix
        )
        if format(pk, self.blockchain.prefix) != memo_key:
            raise InvalidMessageSignature("The signature doesn't match the memo key")

        self.signed_by_account = account
        self.signed_by_name = account["name"]
        self.meta = meta
        self.plain_message = message

        return True
