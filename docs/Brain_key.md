### Brain key
Using brain key object you can get keys(private, public, echorand) in base58 and hex representations.

#### Generating keys example

```python
from echopy import Echo
echo = Echo()
brain_key_object = echo.brain_key()

private_key_base58 = brain_key_object.get_private_key_base58()
private_key_hex = brain_key_object.get_private_key_hex()

echorand_key_base58 = brain_key_object.get_echorand_key_base58()
echorand_key_hex = brain_key_object.get_echorand_key_hex()

public_key_base58 = brain_key_object.get_public_key_base58()
public_key_hex = brain_key_object.get_public_key_hex()
```

#### Set brain key

```python
from echopy import Echo
echo = Echo()
brain_key_object = echo.brain_key()

# set brain key in string format separated by comma or space, or list of string 
brain_key_object.brain_key = "<your brain key>"
```

#### Brain key re-generating

```python
from echopy import Echo
echo = Echo()
brain_key_object = echo.brain_key()
#... some code here

# Switch to another brain_key
brain_key_object = next(brain_key_object)
```