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