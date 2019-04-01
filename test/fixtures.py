from echopy import Echo
import string
import random
from echopy.echoapi.ws.exceptions import RPCError
from echopy.echobase.account import BrainKey
import asyncio

_echo_ws_url = 'wss://testnet.echo-dev.io/ws'
_wif = '5KUbAUeSFgZqMxNKNftxAhhrjrQmgiEE4CXmbdWk8j3MZruCVZe'
_from = '1.2.260'
_to = '1.2.259'


def get_random_asset_symbol():
    asset_symbol_length = random.randint(4, 10)
    asset_symbol = ''.join(random.choice(string.ascii_uppercase) for _ in range(asset_symbol_length))
    return asset_symbol


async def connect_echo(url=_echo_ws_url):
    echo = Echo()
    await echo.connect(url)
    return echo


async def disconnect_echo(echo):
    await echo.disconnect()


async def broadcast_operation(echo, operation_ids, props):
    tx = echo.create_transaction()
    if type(operation_ids) is list:
        assert(len(operation_ids) == len(props))
        for i in range(len(operation_ids)):
            tx = tx.add_operation(name=operation_ids[i], props=props[i])
    else:
        tx = tx.add_operation(name=operation_ids, props=props)
    await tx.sign(_wif)
    return await tx.broadcast()


def get_keys():
    key = BrainKey()

    private_key = str(key.get_private_key())
    public_key = str(key.get_public_key())
    echorand_key = str(key.get_echorand_key())

    return private_key, public_key, echorand_key


def random_string():
    result = ""
    result += "".join(random.choice(string.ascii_letters) for i in range(random.randint(5, 10)))
    return result


def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
