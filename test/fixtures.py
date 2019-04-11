from echopy import Echo
import string
import random


_echo_ws_url = 'wss://testnet.echo-dev.io/ws'
_wif = '5KUbAUeSFgZqMxNKNftxAhhrjrQmgiEE4CXmbdWk8j3MZruCVZe'
_from = '1.2.260'
_to = '1.2.259'


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
