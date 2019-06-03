### Api

This library provides api blockchain methods.

#### Asset Api

```python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
asset_id = '1.3.0'
start = 0
limit = 10
try:
    echo = Echo()
    echo.connect(url)

    all_asset_holders = echo.api.asset.get_all_asset_holders()
    holders_count = echo.api.asset.get_asset_holders_count(asset_id=asset_id)
    asset_holders = echo.api.asset.get_asset_holders(asset_id=asset_id, start=start, limit)

    echo.disconnect()
except Exception as e:
    raise
```

#### Database Api

```python 
from echopy import Echo

url = 'ws://127.0.0.1:9000'
ids = ['1.3.1', '1.3.2']
block_num = 200
try:
    echo = Echo()
    echo.connect(url)

    objects = echo.api.database.get_objects(ids=ids)
    block_header = echo.api.database.get_block_header(block_num=block_num)
    block = echo.api.database.get_block(block_num=block_num)

    echo.disconnect()
except Exception as e:
    raise	
```

#### History Api

```python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
account = '1.2.16'
account_stop = '1.10.0'
account_limit = 100
account_start = '1.10.0'
try:
    echo = Echo()
    echo.connect(url)

    relative_account_history = echo.api.history.get_relative_account_history(account=account)
    account_history = echo.api.history.get_account_history(account=account,
                                                           stop=account_stop,
                                                           limit=account_limit,
                                                           start=account_start)

    echo.disconnect()
except Exception as e:
    raise	
```

#### Network Api

``` python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
try:
    echo = Echo()
    echo.connect(url)
    
    signed_transaction = '<your signed transaction>'
    echo.api.network.broadcast_transaction(signed_transaction=signed_transaction)

    echo.disconnect()
except Exception as e:
    raise
```

#### Registration Api

```python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
name = 'test123'

memo_key = 'ECHO6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV'

try:
    echo = Echo()
    echo.connect(url)
    brain_key = echo.brain_key()
    public_key = get_public_key_base58()
    echo.api.registration.register_account(callback='1',
                                           name=name,
                                           owner_key=public_key,
                                           active_key=public_key,
                                           memo_key=memo_key,
                                           echorand_key=public_key)

    echo.disconnect()
except Exception as e:
    raise                                           
```

---

More information about `API methods` can be browsed by <b><a href="https://echo-dev.io/developers/apis/">link</a></b>.

To `API methods` current coverage status look <b>[Api status](docs/Api_status.md)</b>.
