# CryptoCmpy

- **Author**: `Daniel J. Umpierrez`
- **Site**: [https://github.com/havocesp/cryptocmpy](https://github.com/havocesp/cryptocmpy)
- **License**: `UNLICENSE`
- **Version**: `0.1.1`

# Description
Just another Python 3 "**CryptoCompare**" API wrapper.

# Requirements
 - [python](https://www.python.org/) `(3.5+)`
 - [requests](https://github.com/TODO/requests)
 
# Installation

## _GitHub_ repository (using `pip`)

`$ pip install git+https://github.com/havocesp/cryptocmpy`

# Usage

```python
import time
from cryptocmpy import CryptoCmpy

# amount of seconds calculation for 1 day
day2seconds = 3600 * 24
# current unix datetime format in seconds
epoch = int(time.time())

# from 3 days ago to now as unix epoch
since = epoch - (day2seconds * 3)

cmp = CryptoCmpy()

historic_price = cmp.get_historical_price('BTC', since, 'EUR', 'USD')

print(historic_price)

```

## Changelog

### 0.1.1
- Removed _utils.py_ module
- Minor fixes

### 0.1.0
 - Initial version

# TODO
 - [ ] Complete all REST end points implementation.
