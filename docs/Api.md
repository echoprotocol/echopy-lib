### Api

This library provides api blockchain methods.

#### Asset Api

```python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
echo_asset_id = '1.3.0'

echo = Echo()
echo.connect(url)

all_asset_holders = echo.api.asset.get_all_asset_holders()
echo_asset_holders_count = echo.api.asset.get_asset_holders_count(asset_id=echo_asset_id)

echo.disconnect()
```

#### Database Api

```python 
from echopy import Echo

url = 'ws://127.0.0.1:9000'
object_ids = ['1.2.0', '1.3.0']
block_num = 1

echo = Echo()
echo.connect(url)

objects = echo.api.database.get_objects(object_ids=object_ids)
block_header = echo.api.database.get_block_header(block_num=block_num)
block = echo.api.database.get_block(block_num=block_num)

echo.disconnect()
```

#### History Api

```python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
account = '1.2.16'
stop = '1.6.0'
limit = 100
start = '1.6.0'

echo = Echo()
echo.connect(url)

relative_account_history = echo.api.history.get_relative_account_history(account=account)
account_history = echo.api.history.get_account_history(
    account=account,
    stop=stop,
    limit=limit,
    start=start
)

echo.disconnect()
```

#### Network Api

``` python
from echopy import Echo

url = 'ws://127.0.0.1:9000'

echo = Echo()
echo.connect(url)

signed_transaction = '<your signed transaction>'
echo.api.network.broadcast_transaction(signed_transaction=signed_transaction)

echo.disconnect()
```

#### Registration Api

```python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
name = 'test123'

echo = Echo()
echo.connect(url)

brain_key = echo.brain_key()
public_key = brain_key.get_public_key_base58()

registrar_account = echo.api.registration.get_registrar()

# 1. Account registration (step-by-step actions):
registration_task = echo.api.registration.request_registration_task()

nonce = echo.solve_registration_task(
    block_id=registration_task['block_id'],
    rand_num=registration_task['rand_num'],
    difficulty=registration_task['difficulty']
)

registration_result = echo.api.registration.submit_registration_solution(
    callback='1',
    name=name,
    active=public_key,
    echorand_key=public_key,
    nonce=nonce,
    rand_num=registration_task['rand_num']
)

# 2. Simple account registration:

registration_result = echo.register_account(
    callback='1',
    name=name,
    active=public_key,
    echorand=public_key
)

echo.disconnect()                                    
```

---

More information about `API methods` can be browsed by <b><a href="https://docs.echo.org/api-reference/echo-node-api">link</a></b>.

To `API methods` current coverage status look <b>[Api status](docs/Api_status.md)</b>.
