# Python Library for Echo

Python ECHO library can be used to construct, sign and broadcast transactions and to easily obtain data from the blockchain via public apis.

## Installation

### Install with pip3:

    $ sudo apt-get install libffi-dev libssl-dev python-dev python3-dev python3-pip
    $ pip3 install echopy-lib

### Manual installation:

    $ git clone https://github.com/echoprotocol/echopy-lib.git
    $ cd echopy-lib
    $ python3 setup.py install
    or
    $ pip3 install .

## Preparation

Launched echo node (https://github.com/echoprotocol/echo-core) with open port.

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

To see example of `keys generation`: look <b>[section](docs/Brain_key.md)</b>.

To run `unit tests`:

    $ python3 -m unittest


## Contributing

echopy-lib welcomes contributions from anyone and everyone. Please
see our [guidelines for contributing](CONTRIBUTING.md) and the [code of
conduct](CODE_OF_CONDUCT.md).

### License

A copy of the license is available in the repository's
[LICENSE](LICENSE.txt) file.
