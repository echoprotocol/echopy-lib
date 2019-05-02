from echopy import Echo
import string
import random
from echopy.echobase.account import BrainKey


_echo_ws_url = 'wss://devnet.echo-dev.io/ws'
_wif = 'E7sNmbqX3ZWxBergfa4fG4F2wEzkicpuBzGBtQSNQnHm'
_from = '1.2.45'
_to = '1.2.46'


def get_random_asset_symbol():
    asset_symbol_length = random.randint(4, 10)
    asset_symbol = ''.join(random.choice(string.ascii_uppercase) for _ in range(asset_symbol_length))
    return asset_symbol


def connect_echo(url=_echo_ws_url):
    echo = Echo()
    echo.connect(url)
    return echo


def disconnect_echo(echo):
    echo.disconnect()


def broadcast_operation(echo, operation_ids, props):
    tx = echo.create_transaction()
    if type(operation_ids) is list:
        assert(len(operation_ids) == len(props))
        for i in range(len(operation_ids)):
            tx = tx.add_operation(name=operation_ids[i], props=props[i])
    else:
        tx = tx.add_operation(name=operation_ids, props=props)
    tx.sign(_wif)
    return tx.broadcast()


def get_keys():
    key = BrainKey()

    private_base58 = key.get_private_key_base58()
    public_base58 = key.get_public_key_base58()
    private_hex = key.get_private_key_hex()
    public_hex = key.get_public_key_hex()

    return private_base58, public_base58, private_hex, public_hex


def random_string():
    result = ""
    result += "".join(random.choice(string.ascii_lowercase) for i in range(random.randint(5, 10)))
    return result
