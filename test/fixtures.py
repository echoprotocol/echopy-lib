from echopy import Echo
import string
import random
from echopy.echoapi.ws.exceptions import RPCError
import asyncio

_echo_ws_url = 'wss://devnet.echo-dev.io/ws'
_wif = '5KLRT7oujSYZnDHCJHTDJyuvF2JxBhpQgipEkmM6pVLR6Yh59PF'
_from = '1.2.21'
_to = '1.2.22'


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


def run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)
