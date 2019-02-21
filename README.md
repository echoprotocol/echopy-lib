# Python Library for Echo

Python ECHO library can be used to construct, sign and broadcast transactions and to easily obtain data from the blockchain via public apis.

---
## Installation


### Manual installation:

    $ git clone https://gitlab.pixelplex.by/645.echo/echopy-lib.git
    $ cd echopy-lib
    $ python3 setup.py install

## Usage

```python
from echopy import Echo

url = 'ws://127.0.0.1:9000'
echo = Echo()
echo.connect(url)
accounts = echo.api.database.get_objects(['1.2.0'])
echo.disconnect()

```


To see `Api's` usage examples and information: look <b>[section](docs/Api.md)</b>.

To see `Transactions` usage examples and information: look <b>[section](docs/Transaction.md)</b>.

To run `unit tests`:

```python
python3 -m unittest discover
```

## Contributing

echopy-lib welcomes contributions from anyone and everyone. Please
see our [guidelines for contributing](CONTRIBUTING.md) and the [code of
conduct](CODE_OF_CONDUCT.md).

### License

A copy of the license is available in the repository's
[LICENSE](LICENSE.txt) file.
