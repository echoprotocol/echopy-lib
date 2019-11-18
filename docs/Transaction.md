### Transactions

Using transaction builder you can build and broadcast transaction.

#### Transfer

```python
from echopy import Echo

echo = Echo()
echo.connect(url='ws://127.0.0.1:9000')

account_from = '1.2.20'
account_from_private_key = '<private_key>'
account_to = '1.2.21'

transfer_options = {
    'from': account_from,
    'to': account_to,
    'amount': {
        'asset_id': '1.3.0',
        'amount': 1
    },
    'extensions': [],
}

tx = echo.create_transaction()
tx.add_operation(
    name=echo.config.operation_ids.TRANSFER,
    props=transfer_options
)
tx.add_signer(account_from_private_key)
broadcast_result = tx.broadcast()

echo.disconnect()
```

You can add few operations and signers using this constructions:

```python
tx = echo.create_transaction()
tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)
tx.add_operation(echo.config.operation_ids.TRANSFER, another_transfer_options)
tx.add_signer(first_private_key)
tx.add_signer(second_private_key)
# or
tx = echo.create_transaction()
tx = tx.add_operation(echo.config.operation_ids.TRANSFER , transfer_options)
tx = tx.add_operation(echo.config.operation_ids.TRANSFER, another_transfer_options)
tx = tx.add_signer(first_private_key)
tx = tx.add_signer(second_private_key)

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

More information about `Operations` can be browsed by <b><a href="https://docs.echo.org/api-reference/echo-operations">link</a></b>.

To `Operations` current coverage status look <b>[Operation status](docs/Operations_status.md)</b>.
