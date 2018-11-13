# -*- coding:utf-8 -*-
"""
Cyptocmpy core module.
"""
import collections as col
import pprint
import typing as tp

import requests

_DEBUG = False

_COIN_LIST_URL = '{schema}://www.{domain}/api/data/coinlist/'
# noinspection PyUnusedName
_COIN_SNAPSHOT_FULL_BY_ID_URL = '{schema}://www.{domain}/api/data/coinsnapshotfullbyid/?id='
# noinspection PyUnusedName
_COIN_SNAPSHOT_URL = '{schema}://www.{domain}/api/data/coinsnapshot/'

_PRICE_URL = '{schema}://min-api.{domain}/data/price'
_PRICE_MULTI_URL = '{schema}://min-api.{domain}/data/pricemulti'
# noinspection PyUnusedName
_PRICE_MULTI_FULL_URL = '{schema}://min-api.{domain}/data/pricemultifull'
_PRICE_HISTORICAL_URL = '{schema}://min-api.{domain}/data/pricehistorical'
# noinspection PyUnusedName
_GENERATE_AVG_URL = '{schema}://min-api.{domain}/data/generateAvg'
_DAY_AVG_URL = '{schema}://min-api.{domain}/data/dayAvg'

_SUBS_WATCH_LIST_URL = '{schema}://min-api.{domain}/data/subsWatchlist'
_SUBS_URL = '{schema}://min-api.{domain}/data/subs'

_ALL_EXCHANGES_URL = '{schema}://min-api.{domain}/data/all/exchanges'
# noinspection PyUnusedName
_TOP_EXCHANGES_URL = '{schema}://min-api.{domain}/data/top/exchanges'
# noinspection PyUnusedName
_TOP_VOLUMES_URL = '{schema}://min-api.{domain}/data/top/volumes'
_TOP_PAIRS_URL = '{schema}://min-api.{domain}/data/top/pairs'

_HIST_DAY_URL = '{schema}://min-api.{domain}/data/histoday'
_HIST_HOUR_URL = '{schema}://min-api.{domain}/data/histohour'
_HIST_MINUTE_URL = '{schema}://min-api.{domain}/data/histominute'
# noinspection PyUnusedName
SOCIAL_STATS_URL = '{schema}://www.{domain}/api/data/socialstats?id='
# noinspection PyUnusedName
MINING_CONTRACTS_URL = '{schema}://www.{domain}/api/data/miningcontracts/'
# noinspection PyUnusedName
MINING_EQUIPMENT_URL = '{schema}://www.{domain}/api/data/miningequipment/'


# noinspection PyUnusedFunction,PyPep8Naming,PySameParameterValue
class CryptoCmpy:
    """
    Contains all API urls.
    """
    _BASE = dict(schema='https', domain='cryptocompare.com')

    @classmethod
    def _params(cls, params):
        """

        :param params:
        :type params: dict
        :return:
        """
        params = dict(params or {})

        for param in ['tsyms', 'fsyms']:
            if param in params:
                param_value = params.get(param)
                if isinstance(param_value, str) and ',' not in param:
                    params[param] = [param_value]
                if isinstance(param_value, col.Iterable):
                    params[param] = ','.join([str(s).upper() for s in param_value])

        return params

    @classmethod
    def _query(cls, url, params=None):
        """
        Send query to server and return response.

        :param tp.AnyStr url: URL template.
        :param dict params: parameters used to build URL request.
        :return: request result as dict or list.
        :rtype: dict or list
        """
        params = params or dict()
        url = url.format(**cls._BASE)

        if 'cls' in params:
            del params['cls']
        if 'self' in params:
            del params['self']

        if _DEBUG:
            print(url)
            pprint.pprint(cls._params(params))

        response = requests.get(url, cls._params(params))

        if response.ok:
            raw = response.json()
            return raw.get('Data', raw) if raw.get('Response') != 'Error' else {'Error': raw.get('Message')}
        else:
            response.raise_for_status()

    @classmethod
    def top_pairs(cls, fsym, tsym, limit=5):
        """
        TODO

        :param fsym: from symbol.
        :type fsym: tp.AnyStr
        :param tsym: to symbol.
        :type tsym: tp.AnyStr
        :param int limit: default 5, max 50, min 1
        :return:
        :rtype dict:
        """
        return cls._query(_TOP_PAIRS_URL, locals())

    @classmethod
    def get_price(cls, fsyms, tsyms):
        # noinspection PyUnresolvedReferences
        """
        Price conversion (one to many) from "fsym" currency to "tsyms" currencies.

        >>> data = CryptoCmpy.get_price(fsyms='BTC', tsyms=('ETH', 'USD', 'EUR'))
        >>> isinstance(data, dict)
        True
        >>> all((isinstance(v, float) for v in data.values()))
        True
        >>> data = CryptoCmpy.get_price(('BTC', 'ETH', 'XRP', 'ADA'), ('USD', 'EUR'))
        >>> isinstance(data, dict)
        True
        >>> isinstance(data['total'], float)
        True

        :param fsyms: from currencies.
        :type fsyms: tp.Iterable[tp.AnyStr]
        :param tp.Iterable[tp.AnyStr] tsyms: "to" currencies.
        :return: conversion data result.
        :rtype: tp.Dict
        """
        if isinstance(fsyms, str):
            fsyms = [fsyms]
        if isinstance(tsyms, str):
            tsyms = [tsyms]

        if len(fsyms) == 1 and len(tsyms) >= 1:
            fsym = str(fsyms[0])
            del fsyms
            return cls._query(_PRICE_URL, locals())
        elif len(fsyms) > 1 and len(tsyms) >= 1:
            return cls._query(_PRICE_MULTI_URL, locals())

    @classmethod
    def get_coin_list(cls):
        """
        Returns a dict of dicts containing all currencies metadata.

        >>> data = CryptoCmpy.get_coin_list()
        >>> isinstance(data, dict)
        True

        ... {'Id': '925807',
        ... 'Url': '/coins/csp/overview',
        ... 'ImageUrl': '/media/34478535/csp.png',
        ... 'Name': 'CSP',
        ... 'Symbol': 'CSP',
        ... 'CoinName': 'Caspian',
        ... 'FullName': 'Caspian (CSP)',
        ... 'Algorithm': 'N/A',
        ... 'ProofType': 'N/A',
        ... 'FullyPremined': '0',
        ... 'TotalCoinSupply': '1000000000',
        ... 'BuiltOn': '7605',
        ... 'SmartContractAddress': '0xA6446D655a0c34bC4F05042EE88170D056CBAf45',
        ... 'PreMinedValue': 'N/A',
        ... 'TotalCoinsFreeFloat': 'N/A',
        ... 'SortOrder': '3381',
        ... 'Sponsored': False}

        :return: all crypto currencies with some metadata as dict.
        :rtype: tp.Dict[tp.AnyStr, tp.Dict]
        """
        return cls._query(_COIN_LIST_URL)

    @classmethod
    def get_exchanges_list(cls, exchange=None, base_market=None):
        """
        Return exchanges as list of dict containing some metadata.

        :return: all crypto exchanges with their metadata as dict.
        :rtype: dict
        """
        raw = cls._query(_ALL_EXCHANGES_URL)
        if raw:
            if exchange:
                raw = raw.get(exchange, raw)
            return {k.lower(): v for k, v in raw.items() if base_market and base_market in v}
        else:
            return dict()

    @classmethod
    def get_day_average(cls, fsym, tsym):
        """

        :param fsym: from currency.
        :type fsym: tp.AnyStr
        :param tsym: to currency.
        :type tsym: tp.AnyStr
        :return: dict with day average data.
        :rtype: dict
        """
        return cls._query(_DAY_AVG_URL, locals())

    @classmethod
    def get_watchlist(cls, tsym, *fsyms):
        """

        :param tsym: to currency.
        :rtype tsym: tp.AnyStr
        :param fsyms: from currencies.
        :rtype fsyms: list
        :return:
        :rtype:
        """
        return cls._query(_SUBS_WATCH_LIST_URL, locals())

    @classmethod
    def get_subs(cls, fsym):
        """
        TODO

        :param fsym: from currency.
        :rtype fsym: tp.AnyStr
        :return:
        :rtype:
        """
        return cls._query(_SUBS_URL, locals())

    @classmethod
    def get_day(cls, fsym, tsym, allData=False, toTs=None):
        """

        :param fsym: from symbol.
        :type fsym: tp.AnyStr
        :param tsym:
        :param allData:
        :param toTs:
        :return:
        :rtype: list
        """
        # params = {'fsym': fsym, 'tsym': tsym, 'allData': allData}
        # if toTs:
        #     params.update(toTs=toTs)

        return cls._query(_HIST_DAY_URL, locals())

    @classmethod
    def get_hour(cls, fsym, tsym, limit=168, toTs=None):
        """
        Get OHLC (day candles size)

        :param tsym:
        :type fsym: tp.AnyStr
        :param fsym: from symbol.
        :type fsym: tp.AnyStr
        :param limit:
        :type toTs: int
        :return:
        :rtype: list
        """
        return cls._query(_HIST_HOUR_URL, locals())

    @classmethod
    def get_minute(cls, fsym, tsym, limit=1440, toTs=None):
        """
        Get OHLC (minute candles size)

        :param fsym: from symbol.
        :type fsym: tp.AnyStr
        :param tsym:
        :type fsym: tp.AnyStr
        :param limit:
        :type limit: int
        :param toTs:
        :type toTs: int
        :return:
        :rtype: list
        """
        return cls._query(_HIST_MINUTE_URL, locals())

    @classmethod
    def get_historical_price(cls, fsym, ts, *tsyms):
        """
        Get crypto coin historic price at "sts" timestamp.

        :param fsym: from symbol.
        :type fsym: tp.AnyStr
        :param tsyms:
        :type tsyms:
        :param ts:
        :type ts: int
        :return:
        :rtype:
        """
        return cls._query(_PRICE_HISTORICAL_URL, locals())

    @classmethod
    def get_generate_average(cls, fsym, tsym, markets):
        """

        :param tp.AnyStr fsym:
        :param tp.AnyStr tsym:
        :param markets:
        :return:
        """
        return cls._query(_GENERATE_AVG_URL, locals())

    @classmethod
    def get_exchanges(cls):
        """
        Return exchange list.

        >>> CryptoCmpy.get_exchanges()

        :return:
        """
        return cls._query(_ALL_EXCHANGES_URL)

    # @classmethod
    # def get_exchanges(cls):
    #     """
    #     Return exchange list.
    #
    #     >>> CryptoCmpy.get_exchanges()
    #
    #     :return:
    #     """
    #     return cls._query(_ALL_EXCHANGES_URL)


if __name__ == '__main__':
    print(sorted(CryptoCmpy.get_subs('ZEC')))
