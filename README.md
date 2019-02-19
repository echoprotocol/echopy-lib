# Python Library for Graphene

![](https://img.shields.io/pypi/v/graphenelib.svg?style=for-the-badge)
![](https://img.shields.io/github/downloads/xeroc/python-graphenelib/total.svg?style=for-the-badge)
![](https://img.shields.io/pypi/pyversions/graphenelib.svg?style=for-the-badge)
![](https://img.shields.io/pypi/l/graphenelib.svg?style=for-the-badge)
![](https://cla-assistant.io/readme/badge/xeroc/python-graphenelib)

**Stable**

[![Travis master](https://travis-ci.org/xeroc/python-graphenelib.png?branch=master)](https://travis-ci.org/xeroc/python-graphenelib)
[![docs master](https://readthedocs.org/projects/python-graphenelib/badge/?version=latest)](http://python-graphenelib.readthedocs.io/en/latest/)
[![codecov](https://codecov.io/gh/xeroc/python-graphenelib/branch/master/graph/badge.svg)](https://codecov.io/gh/xeroc/python-graphenelib)


**Develop**

[![Travis develop](https://travis-ci.org/xeroc/python-graphenelib.png?branch=develop)](https://travis-ci.org/xeroc/python-graphenelib)
[![docs develop](https://readthedocs.org/projects/python-graphenelib/badge/?version=develop)](http://python-graphenelib.readthedocs.io/en/develop/)
[![codecov develop](https://codecov.io/gh/xeroc/python-graphenelib/branch/develop/graph/badge.svg)](https://codecov.io/gh/xeroc/python-graphenelib)

---
## Installation


### Manual installation:

    $ git clone https://gitlab.pixelplex.by/645.echo/echopy-lib.git
    $ cd echopy-lib
    $ python3 setup.py install

## Usage

```python
from echo import Echo

url = 'ws://127.0.0.1:9000'
echo = Echo(url)
accounts = echo.api.database.get_object(['1.2.0'])

```


To more examples and options look at section below

To see other `Api's` examples: <b>[section](docs/Api.md)</b>.

To `operations methods` current coverage status look <b>[Api status](docs/Operations_status.md)</b>.

## Contributing

python-bitshares welcomes contributions from anyone and everyone. Please
see our [guidelines for contributing](CONTRIBUTING.md) and the [code of
conduct](CODE_OF_CONDUCT.md).

### License

A copy of the license is available in the repository's
[LICENSE](LICENSE.txt) file.
