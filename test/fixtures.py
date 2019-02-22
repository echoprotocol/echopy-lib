from echopy import Echo
import string
import random

_echo_ws_url = 'wss://devnet.echo-dev.io/ws'
_wif = '5KLRT7oujSYZnDHCJHTDJyuvF2JxBhpQgipEkmM6pVLR6Yh59PF'
_from = '1.2.21'
_to = '1.2.22'

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
