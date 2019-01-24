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

echonet.create_contract(code="608060405234801561001057600080fd5b50610159806100206000396000f300608060405260043610610041576000357c0100000000000000000000000000000000000000000000000000000000900463ffffffff168063dce4a44714610046575b600080fd5b34801561005257600080fd5b50610087600480360381019080803573ffffffffffffffffffffffffffffffffffffffff169060200190929190505050610102565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100c75780820151818401526020810190506100ac565b50505050905090810190601f1680156100f45780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6060813b6040519150601f19601f602083010116820160405280825280600060208401853c509190505600a165627a7a723058200267c4df2b48c4dcdf7624d6d794c3669951bb5142e4bca582a01465c3cdbd670029",
                        registrar="test10123223")

pprint(echonet.broadcast())
