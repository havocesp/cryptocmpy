# -*- coding:utf-8 -*-
"""
Core module.

"""
import pprint

import requests

DEBUG = False

COIN_LIST_URL = '{schema}://www.{domain}/api/data/coinlist/'
# noinspection PyUnusedName
COIN_SNAPSHOT_FULL_BY_ID_URL = '{schema}://www.{domain}/api/data/coinsnapshotfullbyid/?id='
# noinspection PyUnusedName
COIN_SNAPSHOT_URL = '{schema}://www.{domain}/api/data/coinsnapshot/'

PRICE_URL = '{schema}://min-api.{domain}/data/price'
# noinspection PyUnusedName
PRICE_MULTI_URL = '{schema}://min-api.{domain}/data/pricemulti'
# noinspection PyUnusedName
PRICE_MULTI_FULL_URL = '{schema}://min-api.{domain}/data/pricemultifull'
PRICE_HISTORICAL_URL = '{schema}://min-api.{domain}/data/pricehistorical'
# noinspection PyUnusedName
GENERATE_AVG_URL = '{schema}://min-api.{domain}/data/generateAvg'
DAY_AVG_URL = '{schema}://min-api.{domain}/data/dayAvg'

SUBS_WATCH_LIST_URL = '{schema}://min-api.{domain}/data/subsWatchlist'
SUBS_URL = '{schema}://min-api.{domain}/data/subs'
# noinspection PyUnusedName
ALL_EXCHANGES_URL = '{schema}://min-api.{domain}/data/all/exchanges'
# noinspection PyUnusedName
TOP_EXCHANGES_URL = '{schema}://min-api.{domain}/data/top/exchanges'
# noinspection PyUnusedName
TOP_VOLUMES_URL = '{schema}://min-api.{domain}/data/top/volumes'
TOP_PAIRS_URL = '{schema}://min-api.{domain}/data/top/pairs'

HIST_DAY_URL = '{schema}://min-api.{domain}/data/histoday'
HIST_HOUR_URL = '{schema}://min-api.{domain}/data/histohour'
HIST_MINUTE_URL = '{schema}://min-api.{domain}/data/histominute'
# noinspection PyUnusedName
SOCIAL_STATS_URL = '{schema}://www.{domain}/api/data/socialstats?id='
# noinspection PyUnusedName
MINING_CONTRACTS_URL = '{schema}://www.{domain}/api/data/miningcontracts/'
# noinspection PyUnusedName
MINING_EQUIPMENT_URL = '{schema}://www.{domain}/api/data/miningequipment/'


# noinspection PyUnusedFunction,PyPep8Naming,PySameParameterValue
class CryptoCmp:
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
                if isinstance(params[param]):
                    params[param] = [params[param]]
                params[param] = [s.upper() for s in params[param]]
                params[param] = ','.join(params[param])

        return params

    @classmethod
    def _url(cls, template):
        """
        Return base URL.

        :param template: template URL
        :type template: str
        :return: filled template URL as str
        :rtype: str
        """
        return template.format(**cls._BASE)

    @classmethod
    def _query(cls, url, params=None):
        """
        Send query to server and return response.

        :param url: URL template.
        :type url:str
        :param params: parameters used to build URL request.
        :type params: dict
        :return:
        :rtype: dict or list
        """
        params = params or dict()
        url = url.format(**cls._BASE)

        if DEBUG:
            print(url)
            pprint.pprint(cls._params(params))

        response = requests.get(url, cls._params(params))

        if response.ok:
            raw = response.json()
            return raw.get('Data', raw)
        else:
            response.raise_for_status()

    @classmethod
    def top_pairs(cls, fsym, tsym, limit=5):
        """
        TODO

        :param fsym: from symbol.
        :type fsym: str
        :param tsym: to symbol.
        :type tsym: str
        :param int limit: default 5, max 50, min 1
        :return:
        :rtype dict:
        """
        return cls._query(TOP_PAIRS_URL, locals())

    @classmethod
    def get_price(cls, fsym, *tsyms):
        """
        Price conversion (one to many) from "fsym" to "fsyms"

        :param fsym: from currency.
        :type fsym: str
        :param tsyms:  to currencies.
        :type tsyms: list
        :return: conversion data result.
        :rtype: dict
        """
        return cls._query(PRICE_URL, locals())

    @classmethod
    def get_coin_list(cls):
        """
        Return currencies as list of dict containing some metadata.

        :return: list of crypto currencies with some metadata as dict.
        :rtype: list
        """
        return cls._query(COIN_LIST_URL)

    @classmethod
    def get_exchanges_list(cls, exchange=None, base_market=None):
        """
        Return exchanges as list of dict containing some metadata.

        :return: list of crypto exchanges with some metadata as dict.
        :rtype: dict
        """
        raw = cls._query(ALL_EXCHANGES_URL)
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
        :type fsym: str
        :param tsym: to currency.
        :type tsym: str
        :return: dict with day average data.
        :rtype: dict
        """
        return cls._query(DAY_AVG_URL, locals())

    @classmethod
    def get_watchlist(cls, tsym, *fsyms):
        """

        :param tsym: to currency.
        :rtype tsym: str
        :param fsyms: from currencies.
        :rtype fsyms: list
        :return:
        :rtype:
        """
        return cls._query(SUBS_WATCH_LIST_URL, locals())

    @classmethod
    def get_subs(cls, fsym):
        """
        TODO

        :param fsym: from currency.
        :rtype fsym: str
        :return:
        :rtype:
        """
        return cls._query(SUBS_URL, locals())

    @classmethod
    def get_day(cls, fsym, tsym, allData=False, toTs=None):
        """

        :param fsym: from symbol.
        :type fsym: str
        :param tsym:
        :param allData:
        :param toTs:
        :return:
        :rtype: list
        """
        # params = {'fsym': fsym, 'tsym': tsym, 'allData': allData}
        # if toTs:
        #     params.update(toTs=toTs)

        return cls._query(HIST_DAY_URL, locals())

    @classmethod
    def get_hour(cls, fsym, tsym, limit=168, toTs=None):
        """
        Get OHLC (day candles size)

        :param tsym:
        :type fsym: str
        :param fsym: from symbol.
        :type fsym: str
        :param limit:
        :type toTs: int
        :return:
        :rtype: list
        """
        return cls._query(HIST_HOUR_URL, locals())

    @classmethod
    def get_minute(cls, fsym, tsym, limit=1440, toTs=None):
        """
        Get OHLC (minute candles size)

        :param fsym: from symbol.
        :type fsym: str
        :param tsym:
        :type fsym: str
        :param limit:
        :type limit: int
        :param toTs:
        :type toTs: int
        :return:
        :rtype: list
        """
        return cls._query(HIST_MINUTE_URL, locals())

    @classmethod
    def get_historical_price(cls, fsym, ts, *tsyms):
        """
        Get crypto coin historic price at "sts" timestamp.

        :param fsym: from symbol.
        :type fsym: str
        :param tsyms:
        :type tsyms:
        :param ts:
        :type ts: int
        :return:
        :rtype:
        """
        return cls._query(PRICE_HISTORICAL_URL, locals())

    @classmethod
    def get_generate_average(cls, fsym, tsym, markets):
        """

        :param fsym:
        :param tsym:
        :param markets:
        :return:
        """
        return cls._query(GENERATE_AVG_URL, locals())


if __name__ == '__main__':
    cmd = Base()
    # result = cmd.get_day('BTC', 'USD', toTs=1512065120)
    by_exchange_coinlist = cmd.get_exchanges_list('Binance', 'USDT')

    pprint.pprint(by_exchange_coinlist)
