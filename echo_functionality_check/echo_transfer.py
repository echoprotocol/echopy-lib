from bitshares import BitShares
from pprint import pprint

# connect to testnet
echonet = BitShares(
    "ws://195.201.164.54:6311/",
    bundle=True,
)

if not echonet.wallet.created():

    # create local wallet , set passphrase
    echonet.wallet.create('qwe')
    # connect local wallet to testnet wallet using PrivateKey
    echonet.wallet.addPrivateKey('5KYZdUEo39z3FPrtuX2QbbwGnNP5zTd7yyr2SC1j299sBCnWjss')

# unlock wallet using secret passphrase
echonet.wallet.unlock('qwe')

echonet.transfer("qweasd123", 1, "ECHO", account="test10123223")

pprint(echonet.broadcast())
