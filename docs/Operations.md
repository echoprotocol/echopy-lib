### Transactions

Using transaction builder you can build and broadcast transaction

#### Transfer

```python
from echo import Echo
from echobase.config import *

echo = Echo(node='ws://127.0.0.1:9000')

transfer_options = {
    'fee': { # optional, default fee asset: 1.3.0, amount: will be calculated
        'asset_id': '1.3.0'        
    },
    'from': '1.2.20',
    'to': '1.2.21',
    'amount': {
        'asset_id': '1.3.0',
        'amount': 1
    },
    'memo': { # optional
        'from': 'ECHO6tMhKMDpynSsLyFL3gk2gZi4xMayficom97fZQKh64FHtCpV7D', # memo key
        'to': 'ECHO8gP5V1F9cudUHxxoDb66BwiEPUB4ZQmwgtLXDrXaQAuJWb921w', # memo key
        'nonce': 424252442,
        'message': '746573745F6D657373616765', # hex string
    },
    'extensions': [],
}

tx = echo.create_transaction()
tx.add_operation(name=operations_ids.transfer, props=transfer_options)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()
tx.broadcast()

```

#### Create contract

```python
from echo import Echo
from echobase.config import *

echo = Echo(node='ws://127.0.0.1:9000')

bytecode = '...' # contract bytecode 
constructor_parameters = '...' # constructor parameters

create_contract_props = {
     # fee optional, default fee asset: 1.3.0, amount: will be calculated
    'registrar': '1.2.20',
    'value': { 'asset_id': '1.3.0', 'amount': 1 }, # transfer asset to contract
    'gasPrice': 0,
    'gas': 1e7,
    'code': bytecode + constructor_parameters
    'supported_asset_id': '1.3.0',
    'eth_accuracy': False,
}

tx = echo.create_transaction()
tx.add_operation(name=operations_ids.create_contract, props=create_contract_props)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()

tx.broadcast()
```

#### Call contract

```python
from echo import Echo
from echobase.config import *

echo = Echo(node='ws://127.0.0.1:9000')

method = '...' # method
method_parameters = '...' # parameters 

call_contract_props = {
    # fee optional, default fee asset: 1.3.0, amount: will be calculated
    'registrar': '1.2.20',
    'value': { # if method mark as payable you can transfer asset, if not set amount to 0
        'asset_id': '1.3.0',
        'amount': 1,
    },
    'gasPrice': 0,
    'gas': 1e7,
    'code': method + method_parameters
    'callee': '1.16.20',
}

tx = echo.create_transaction()
tx.add_operation(name=operations_ids.call_contract, props=call_contract_props)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()

tx.broadcast()
```

#### Create asset

```python
from echo import Echo
from echobase.config import *

echo = Echo(node='ws://127.0.0.1:9000')

create_asset_props = {
    # fee optional, default fee asset: 1.3.0, amount: will be calculated
    'issuer': '1.2.20',
    'symbol': 'NEWASSET',
    'precision': 5,
    'common_options': {
        'max_supply': 1000000000000000,
        'market_fee_percent': 0,
        'max_market_fee': 1000000000000000,
        'issuer_permissions': 79,
        'flags': 0,
        'core_exchange_rate': {
            'base': {
                'amount': 10,
                'asset_id': '1.3.0',
            },
            'quote': {
                'amount': 1,
                'asset_id': '1.3.1',
            }
        },
        'whitelist_authorities': [],
        'blacklist_authorities': [],
        'whitelist_markets': [],
        'blacklist_markets': [],
        'description': '',
    },
    # bitasset_opts optional
    'is_prediction_market': False,
}

tx = echo.create_transaction()
tx.add_operation(name=operations_ids.create_asset, props=create_asset_props)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()

tx.broadcast()
```

You can add few operations and signers using this constructions:

```python
tx = echo.create_transaction()
tx.add_operation(operations_ids.transfer, transfer_options)
tx.add_operation(=operations_ids.call_contract, call_contract_props)
tx.add_signer(private_key) #private_key first
tx.add_signer(private_key) #private_key second
# or
tx = echo.create_transaction()
tx = tx.add_operation(operations_ids.transfer, transfer_options)
tx = tx.add_operation(=operations_ids.call_contract, call_contract_props)
tx = tx.add_signer(private_key) #private_key first
tx = tx.add_signer(private_key) #private_key second

broadcast_result = tx.broadcast()
```

If you have only one signer you can reduce parts of code:

```python
tx = echo.create_transaction()
tx.add_operation(operations_ids.transfer, transfer_options)
# or 
tx = echo.create_transaction()
tx = tx.add_operation(operations_ids.transfer, transfer_options)

broadcast_result = tx.broadcast(private_key)
```

Or sign first and then broadcast:

```python
tx = echo.create_transaction()
tx.add_operation(operations_ids.transfer, transfer_options)
tx.sign(private_key)
# or 
tx = echo.create_transaction()
tx = tx.add_operation(operations_ids.transfer, transfer_options)
tx = tx.sign(private_key)

broadcast_result = tx.broadcast()
```
