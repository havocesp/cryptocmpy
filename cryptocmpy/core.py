# -*- coding:utf-8 -*-
"""Cyptocmpy core module."""
import collections as col
import json
import sys
from typing import Union as U, Text as Str, Sequence as Seq, Dict, List

import requests

# _COIN_SNAPSHOT_FULL_BY_ID_URL = 'https://www.cryptocompare.com/api/data/coinsnapshotfullbyid/?id='
# _COIN_SNAPSHOT_URL = 'https://www.cryptocompare.com/api/data/coinsnapshot/'
# SOCIAL_STATS_URL = 'https://www.cryptocompare.com/api/data/socialstats?id='
# MINING_CONTRACTS_URL = 'https://www.cryptocompare.com/api/data/miningcontracts/'
# MINING_EQUIPMENT_URL = 'https://www.cryptocompare.com/api/data/miningequipment/'
from model import Feeds, Categories, Coin, NewsItem

_DEBUG = False

_BASE = 'https://min-api.cryptocompare.com{}'
_COIN_LIST_URL = '/data/all/coinlist'

_PRICE_URL = '/data/price/'
_PRICE_MULTI_URL = '/data/pricemulti'

_PRICE_MULTI_FULL_URL = '/data/pricemultifull'
_PRICE_HISTORICAL_URL = '/data/pricehistorical'

_GENERATE_AVG_URL = '/data/generateAvg'
_DAY_AVG_URL = '/data/dayAvg'

_SUBS_WATCH_LIST_URL = '/subsWatchlist'
_SUBS_URL = '/subs'

_EXCHANGES_ALL_URL = '/data/all/exchanges'
_EXCHANGES_GENERAL_URL = '/data/exchanges/general'
_EXCHANGES_TOP_URL = '/data/top/exchanges'

_TOP_VOLUMES_URL = '/data/top/volumes'
_TOP_PAIRS_URL = '/data/top/pairs'

_HIST_DAY_URL = '/data/histoday'
_HIST_HOUR_URL = '/data/histohour'
_HIST_MINUTE_URL = '/data/histominute'

_RATE_LIMIT_URL = '/stats/rate/limit'

_NEWS = '/data/v2/news/'
_NEWS_FEEDS = '/data/news/feeds'
_NEWS_CATEGORIES = '/data/news/categories'
_NEWS_FEEDS_AND_CATEGORIES = '/data/news/feedsandcategories'

_SOCIAL_STATS_COIN = '/data/social/coin/latest'
_SOCIAL_STATS_HOUR = '/data/social/coin/histo/hour'
_SOCIAL_STATS_DAY = '/data/social/coin/histo/day'


def _params(params) -> Dict:
    """Params handler.

    :param Dict params: params to be handled.
    :return: params after handling as dict.
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


def _query(url, params=None) -> U[Dict, List]:
    """Send query to server and return response.

    :param Text url: URL css.
    :param Dict params: parameters used to build URL request.
    :return: request result as dict or list.
    """
    result = None
    params = dict(params or {})

    if 'cls' in params:
        del params['cls']
    if 'self' in params:
        del params['self']

    url = _BASE.format(url)

    response = requests.get(url, _params(params), timeout=60)

    if response.ok:
        try:
            raw = response.json()
            if isinstance(raw, list):
                result = raw
            elif raw.get('Response', '') == 'Success' or 'success' in raw.get('Message', ''):
                result = raw.get('Data', raw)
            else:
                result = {'Error': raw.get('Message', 'Unknown')}
        except requests.RequestException as err:
            result = {'Error': 'Request failed'}
            print(f' - [ERROR] Request failed.\n - Details: {str(err)}', file=sys.stderr)
        except json.JSONDecodeError:
            result = {'Error': 'Received data could not be parsed (not JSON?).'}
            print(' - [ERROR] JSON data could not be parsed.', file=sys.stderr)
    else:
        response.raise_for_status()

    return result or dict()


class CryptoSocialStats:

    def __init__(self, api_key):
        self.api_key = str(api_key)

    def stats_coin(self, coinId=1182):
        """Get the latest social stats data for a coin.

        :param coinId: the id of the coin you want data for (default 1182).
        :return: latest social stats data for the coin requested.
        """
        return _query(_SOCIAL_STATS_COIN, {'api_key': self.api_key, **locals()})

    def stats_coin_hour(self,
                        coinId=1182,
                        aggregate=1,
                        aggregatePredictableTimePeriods=True,
                        limit=30,
                        toTs=None):
        """Get hourly social stats data for a coin.

        :param coinId: the id of the coin you want data for (default 1182).
        :param aggregate: time period to aggregate the data over from 1 to 30 (default 1)
        :param aggregatePredictableTimePeriods: (only with aggregate in use)
        :param int limit: number of rows to return from 1 to 2000 (default 30)
        :param toTs: returns historical data before that timestamp.
        :return: hourly social stats data for the coin requested.
        """
        return _query(_SOCIAL_STATS_HOUR, {'api_key': self.api_key, **locals()})

    def stats_coin_day(self,
                       coinId=1182,
                       aggregate=1,
                       aggregatePredictableTimePeriods=True,
                       limit=30,
                       toTs=None):
        """Get daily social stats data for a coin.

        :param coinId: the id of the coin you want data for (default 1182).
        :param aggregate: time period to aggregate the data over from 1 to 30 (default 1)
        :param aggregatePredictableTimePeriods: (only with aggregate in use)
        :param int limit: number of rows to return from 1 to 2000 (default 30)
        :param toTs: returns historical data before that timestamp.
        :return: returns daily social stats data for the coin requested.
        """
        return _query(_SOCIAL_STATS_DAY, {'api_key': self.api_key, **locals()})


class CryptoNews:

    @classmethod
    def get_news(cls, feeds=None, categories=None, excludeCategories=None, lTs=0, lang=None, sortOrder=None) -> List[
        NewsItem]:
        """Retrieve news from feeds.

        :param feeds:               set specific feeds where where news will be retrieved
        :param categories:          category of news articles to return
        :param excludeCategories:   news article categories to exclude from results
        :param lTs:	                returns news before the supplied timestamp.
        :param lang:                news language filter (Eng[EN], Portuguese [PT] and Spain[ES])
        :param sortOrder:           the order to return news articles. Accepted values: "latest" or "popular"
        :return:                    received news raw data as dict type.
        """
        feeds = str(feeds or 'ALL_NEWS_FEEDS')
        categories = str(categories or 'ALL_NEWS_CATEGORIES')
        excludeCategories = str(excludeCategories or 'NO_EXCLUDED_NEWS_CATEGORIES')
        lang = str(lang or 'EN')
        sortOrder = str(sortOrder or 'latest')
        result = _query(_NEWS, locals())
        return [NewsItem(**r) for r in result]

    @classmethod
    def get_feeds(cls):
        """Query and return all news feeds."""
        return Feeds(_query(_NEWS_FEEDS))

    @classmethod
    def get_categories(cls):
        """Query and return all news categories."""
        return Categories(_query(_NEWS_CATEGORIES))

    @classmethod
    def get_feeds_and_categories(cls):
        """Query and return all news feeds and categories at once."""
        raw = _query(_NEWS_FEEDS_AND_CATEGORIES)
        raw.update(Categories=Categories(raw), Feeds=Feeds(raw))
        return raw


class CryptoCmpy:
    """CryptoCompare API Wrapper."""

    @classmethod
    def top_pairs(cls, fsym, tsym, limit=5) -> Dict:
        """Get top volume based pairs.

        :param tp.Text fsym: from symbol.
        :param tp.Text tsym: to symbol.
        :param int limit: default 5, max 50, min 1
        :return:top volume based pairs.
        """
        return _query(_TOP_PAIRS_URL, locals())

    @classmethod
    def get_price(cls, fsyms: U[Seq[Str], Str], tsyms: U[Seq[Str], Str]) -> Dict:
        """Price conversion (one to many) from "fsym" currency to "tsyms" currencies.

        >>> data = CryptoCmpy.get_price(fsyms='BTC', tsyms=('ETH', 'USD', 'EUR'))
        >>> isinstance(data, dict)
        True
        >>> all(isinstance(v, float) for v in data.values())
        True
        >>> data = CryptoCmpy.get_price(('BTC', 'ETH', 'XRP', 'ADA'), ('USD', 'EUR'))
        >>> isinstance(data, dict)
        True
        >>> isinstance(data['total'], float)
        True
        """
        if isinstance(fsyms, str):
            fsyms = [fsyms]

        if isinstance(tsyms, str):
            tsyms = [tsyms]

        if len(fsyms) == 1 and len(tsyms) >= 1:
            fsym = str(fsyms[0])
            del fsyms
            return _query(_PRICE_URL, locals())
        elif len(fsyms) > 1 and len(tsyms) >= 1:
            return _query(_PRICE_MULTI_URL, locals())
        else:
            raise ValueError('Bad num or params.')

    @classmethod
    def get_coin_list(cls) -> List[Coin]:
        """Returns a dict of dicts containing all currencies metadata.

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
        ... 'SmartContractAddress': '0xA6446D655a0c34bC4F05042EE88170D056CBAf4',
        ... 'PreMinedValue': 'N/A',
        ... 'TotalCoinsFreeFloat': 'N/A',
        ... 'SortOrder': '3381',
        ... 'Sponsored': False}

        :return: all crypto currencies with some metadata as dict.
        :rtype: Dict[Str, Dict]
        """
        raw = _query(_COIN_LIST_URL)
        return [Coin(**r) for r in raw.values()]

    @classmethod
    def get_exchanges_metadata(cls, exchange=None) -> Dict:
        """Return exchanges as list of dict containing some metadata.

        :return: all crypto exchanges with their metadata as dict.
        """
        result = _query(_EXCHANGES_GENERAL_URL)
        if result:
            if exchange:
                result = result.get(exchange, result)
            return {k.lower(): v for k, v in result.items()}
        else:
            return dict()

    @classmethod
    def get_exchanges_list(cls, exchange=None, base_market=None) -> Dict:
        """Return exchanges as list of dict containing some metadata.

        :return: all crypto exchanges with their metadata as dict.
        """
        raw = _query(_EXCHANGES_ALL_URL)
        if raw:
            if exchange:
                raw = raw.get(exchange, raw)
            return {k.lower(): v for k, v in raw.items() if base_market and base_market in v}
        else:
            return dict()

    @classmethod
    def get_day_average(cls, fsym, tsym) -> Dict:
        """Get day average for specified symbols.

        :param Str fsym: from currency.
        :param Str tsym: to currency.
        :return: dict with day average data.
        """
        return _query(_DAY_AVG_URL, locals())

    @classmethod
    def get_watchlist(cls, tsym, *fsyms) -> List:
        """Get watch list.

        :param Str tsym: to currency.
        :param List fsyms: from currencies.
        :return: watch list.
        """
        return _query(_SUBS_WATCH_LIST_URL, locals())

    @classmethod
    def get_subs(cls, fsym) -> U[Dict, List]:
        """TODO

        :param Str fsym: from currency.
        :return:
        """
        return _query(_SUBS_URL, locals())

    @classmethod
    def get_day(cls, fsym, tsym, allData=False, toTs=None) -> List:
        """Get OHLC (day candles size)

        :param Str fsym: from symbol.
        :param Str tsym: to symbol.
        :param bool allData: if true all data will be retrieve.
        :param int toTs: ending time as timestamp.
        :return: day candles as list.
        """
        params = {'fsym': fsym, 'tsym': tsym, 'allData': allData}
        if toTs:
            params.update(toTs=toTs)

        return _query(_HIST_DAY_URL, locals())

    @classmethod
    def get_hour(cls, fsym, tsym, limit=168, toTs=None) -> List:
        """Get OHLC (hour candles size)

        :param Str tsym: to symbol.
        :param Str fsym: from symbol.
        :param Str limit: max or rows to retrieve.
        :param int toTs: ending time as timestamp.
        :return: hourly candles.
        """
        return _query(_HIST_HOUR_URL, locals())

    @classmethod
    def get_minute(cls, fsym, tsym, limit=1440, toTs=None) -> List:
        """Get OHLC (minute candles size)

        :param Str fsym: from symbol.
        :param Str tsym:
        :param int limit:
        :param int toTs: ending time as timestamp.
        :return:
        """
        return _query(_HIST_MINUTE_URL, locals())

    @classmethod
    def get_rate_limit_info(cls, calls_left=True):
        """Get detailed info about your API usage.

        Dict type instance with info about calls already made and calls left in the last second, minute, hour, day and month
        as dict with keys  and in the other hand a detailed "left" about user rate limit, this is, c info by time periods.

        :param bool calls_left: a switch  set to False, calls left info by periods, otherwise info will be about calls made.
        :return:
        """
        result = _query(_RATE_LIMIT_URL)
        return result[f'calls_{"left" if calls_left else "made"}']

    @classmethod
    def get_historical_price(cls, fsym, ts, *tsyms):
        """Get crypto coin historic price at "ts" timestamp.

        :param Str fsym: from symbol.
        :param Seq tsyms:
        :param int ts: time as timestamp.
        :return:
        """
        return _query(_PRICE_HISTORICAL_URL, locals())

    @classmethod
    def get_generate_average(cls, fsym, tsym, markets):
        """Get generate average for symbols.

        :param Str fsym: from symbol.
        :param Str fsym: to symbol.
        :param markets:
        :return:
        """
        return _query(_GENERATE_AVG_URL, locals())

    @classmethod
    def get_exchanges(cls) -> List:
        """Return exchange list.

        >>> lst = CryptoCmpy.get_exchanges()
        >>> isinstance(lst, list) and len(lst) > 0
        True

        :return: exchange list
        """
        return _query(_EXCHANGES_ALL_URL)


if __name__ == '__main__':
    # pprint(CryptoCmpy.get_coin_list())
    # pprint(CryptoSocialStats(api_key).stats_coin_day())
    # feeds_and_categories = CryptoNews.get_feeds_and_categories()
    news = CryptoNews.get_news(lang='ES') + CryptoNews.get_news(lang='EN')

    for n in sorted(news, key=lambda n: n.published_on.timestamp(), reverse=True):
        title = n.title if len(n.title) < 90 else f'{n.title[:90]} ...'
        # url = n.url.replace('http://', '').replace('https://', '')
        print(f'[{n.published_on:%d-%b %H:%M}] {title:<94} - {n.url:<}')
    # feeds_and_categories = CryptoNews.get_feeds_and_categories()
    # print(Feeds(feeds_and_categories))
    # pprint(Feeds(feeds_and_categories))
#     from datetime import datetime as dt
#
#     ts = dt.strptime('04-06-2019', '%d-%m-%Y').timestamp()
#     print(CryptoCmpy.get_historical_price('BTC', int(ts), 'USD'))
