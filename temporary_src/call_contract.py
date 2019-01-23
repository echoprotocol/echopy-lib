from bitshares import BitShares

# connect to testnet
echonet = BitShares(
    "ws://195.201.164.54:6311/",
    bundle=True,
)

if not echonet.wallet.created():
    echonet.wallet.create('qwe')
    echonet.wallet.addPrivateKey('5KYZdUEo39z3FPrtuX2QbbwGnNP5zTd7yyr2SC1j299sBCnWjss')

echonet.wallet.unlock('qwe')

#echonet.create_account(account_name='yarosalv', registrar ="1.2.0", owner_key='ECHO5WeESxRb9ftmjcGYptTSi59ygWWECBbPZSRVjyNang36dcM6XY',
#   active_key='ECHO5WeESxRb9ftmjcGYptTSi59ygWWECBbPZSRVjyNang36dcM6XY', memo_key='ECHO5WeESxRb9ftmjcGYptTSi59ygWWECBbPZSRVjyNang36dcM6XY')

echonet.call_contract(code="dce4a447000000000000000000000000010000000000000000000000000000000000006a",
                      registrar="1.2.16", callee="1.16.106")

print(echonet.broadcast())
