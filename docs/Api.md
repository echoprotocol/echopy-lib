### Api
This library provides api blockchain methods.

#### Asset Api

```python
from echo import Echo

url = 'ws://127.0.0.1:9000'
asset_id = '1.3.0'
start = 0
limit = 10
try:
    echo = Echo(url)
    all_asset_holders = echo.api.asset.get_all_asset_holders()
    holders_count = echo.api.asset.get_asset_holders_count(asset_id=asset_id)
    asset_holders = echo.api.asset.get_asset_holders(asset_id=asset_id, start=start, limit)
except Exception as e:
    raise
```

#### Database Api

```python 
from echo import Echo

url = 'ws://127.0.0.1:9000'
ids = ['1.3.1', '1.3.2']
block_num = 200
try:
    echo = Echo(url)
    objects = echo.api.database.get_objects(ids=ids)
    block_header = echo.api.database.get_block_header(block_num=block_num)
    block = echo.api.database.get_block(block_num=block_num)
except Exception as e:
    raise	
```

#### History Api

```python
from echo import Echo

url = 'ws://127.0.0.1:9000'
account = '1.2.16'
account_stop = '1.11.0'
account_limit = 100
account_start = '1.11.0'
try:
    echo = Echo(url)
    relative_account_history = echo.api.history.get_relative_account_history(account=account)
    account_history = echo.api.history.get_account_history(account=account,
                                                           stop=account_stop,
                                                           limit=account_limit,
                                                           start=account_start)
except Exception as e:
    raise	
```

#### Network_broadcast Api

``` python
from echo import Echo

url = 'ws://127.0.0.1:9000'
signed_transaction = '2.7.1'
try:
    echo = Echo(url)
    echo.api.network_broadcast.broadcast_transaction(signed_transaction=signed_transaction)
except Exception as e:
    raise
```

#### Registration Api

```python
from echo import Echo

url = 'ws://127.0.0.1:9000'
name = 'test123'
owner_key = 'ECHO6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV'
active_key = 'ECHO6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV'
memo_key = 'ECHO6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV'
echorand_key = 'DETDvHDsAfk2M8LhYcxLZTbrNJRWT3UH5zxdaWimWc6uZkH'

try:
    echo = Echo(url)
    echo.api.registration.register_account(name=name,
                                           owner_key=owner_key,
                                           active_key=active_key,
                                           memo_key=memo_key,
                                           echorand_key=echorand_key)
except Exception as e:
    raise                                           
```

---

More info about `API methods` can be browsed by <i><b><a href="https://echo-dev.io/developers/apis/">link</a></b></i>.

To `API methods` current coverage status look <b>[Api status](docs/Api_status.md)</b>.
