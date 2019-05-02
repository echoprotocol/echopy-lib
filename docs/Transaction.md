### Transactions

Using transaction builder you can build and broadcast transaction.

#### Transfer

```python
from echopy import Echo

echo = Echo()
echo.connect(url='ws://127.0.0.1:9000')

operation_id = echo.config.operation_ids.TRANSFER 

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
    'extensions': [],
}

tx = echo.create_transaction()
tx.add_operation(name=operation_id, props=transfer_options)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()

broadcast_result = tx.broadcast()

echo.disconnect()
```

#### Create contract

```python
from echopy import Echo

echo = Echo()
echo.connect(url='ws://127.0.0.1:9000')

operation_id = echo.config.operation_ids.CREATE_CONTRACT 

bytecode = '...' # contract bytecode 
constructor_parameters = '...' # constructor parameters

create_contract_props = {
     # fee optional, default fee asset: 1.3.0, amount: will be calculated
    'registrar': '1.2.20',
    'value': { 'asset_id': '1.3.0', 'amount': 1 }, # transfer asset to contract
    'code': bytecode + constructor_parameters
    'supported_asset_id': '1.3.0',
    'eth_accuracy': False,
}

tx = echo.create_transaction()
tx.add_operation(name=operation_id, props=create_contract_props)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()

broadcast_result = tx.broadcast()

echo.disconnect()
```

#### Call contract

```python
from echopy import Echo

echo = Echo()
echo.connect(url='ws://127.0.0.1:9000')

operation_id = echo.config.operation_ids.CALL_CONTRACT 

method = '...' # method
method_parameters = '...' # parameters 

call_contract_props = {
    # fee optional, default fee asset: 1.3.0, amount: will be calculated
    'registrar': '1.2.20',
    'value': { # if method mark as payable you can transfer asset, if not set amount to 0
        'asset_id': '1.3.0',
        'amount': 1,
    },
    'code': method + method_parameters
    'callee': '1.14.20',
}

tx = echo.create_transaction()
tx.add_operation(name=operation_id, props=call_contract_props)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()

broadcast_result = tx.broadcast()

echo.disconnect()
```

#### Asset create

```python
from echopy import Echo

echo = Echo()
echo.connect(url='ws://127.0.0.1:9000')

operation_id = echo.config.operation_ids.ASSET_CREATE

create_asset_props = {
    # fee optional, default fee asset: 1.3.0, amount: will be calculated
    'issuer': '1.2.20',
    'symbol': 'NEWASSET',
    'precision': 5,
    'common_options': {
        'max_supply': 1000000000000000,
        'market_fee_percent': 0,
        'max_market_fee': 1000000000000000,
        'issuer_permissions': 78,
        'flags': 0,
        'core_exchange_rate': {
            'base': {
                'amount': 10,
                'asset_id': '1.3.0',
            },
            'quote': {
                'amount': 2,
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
tx.add_operation(name=operation_id, props=create_asset_props)
tx.add_signer('5J95jcWeqxqRK6McNp3MLi5yEzeWCHsNpe72iw9QphXfUwpz84v')
tx.sign()

broadcast_result = tx.broadcast()

echo.disconnect()
```

You can add few operations and signers using this constructions:

```python
tx = echo.create_transaction()
tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)
tx.add_operation(echo.config.operation_ids.CALL_CONTRACT, call_contract_props)
tx.add_signer(private_key) #private_key first
tx.add_signer(private_key) #private_key second
# or
tx = echo.create_transaction()
tx = tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)
tx = tx.add_operation(echo.config.operation_ids.CALL_CONTRACT, call_contract_props)
tx = tx.add_signer(private_key) #private_key first
tx = tx.add_signer(private_key) #private_key second

broadcast_result = tx.broadcast()
```

If you have only one signer you can reduce parts of code:

```python
tx = echo.create_transaction()
tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)
# or 
tx = echo.create_transaction()
tx = tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)

broadcast_result = tx.broadcast(private_key)
```

Or sign first and then broadcast:

```python
tx = echo.create_transaction()
tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)
tx.sign(private_key)
# or 
tx = echo.create_transaction()
tx = tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)
tx = tx.sign(private_key)

broadcast_result = tx.broadcast()
```

---

More information about `Operations` can be browsed by <b><a href="https://echo-dev.io/developers/operations/">link</a></b>.

To `Operations` current coverage status look <b>[Operation status](docs/Operations_status.md)</b>.
