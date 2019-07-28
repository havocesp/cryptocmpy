# -*- coding:utf-8 -*-
"""CryptoCmpy model module.

Python 3 "CryptoCompare" site API wrapper.
"""
import json
from collections import UserList
from datetime import datetime as dt
from typing import Dict, Text as Str

from utils import snake_case, type_parser


class NewsBase:
    name: Str

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'{type(self).__name__}[{self.name}]'

    def to_dict(self):
        T = type(self)
        return {k: v for k, v in vars(self).items() if k[0] != '_'}


class NewsItem:
    class Source:
        def __init__(self, **kwargs):
            self.name = kwargs.get('name')
            self.lang = kwargs.get('lang')
            self.url = kwargs.get('url')

    def __init__(self, **kwargs):
        kwargs = {k: type_parser(v) for k, v in kwargs.items()}
        self.id = kwargs.get('id')
        self.guid = kwargs.get('guid')
        self.published_on = dt.fromtimestamp(kwargs.get('published_on'))
        self.imageurl = kwargs.get('imageurl')
        self.title = kwargs.get('title')
        self.url = kwargs.get('url')
        self.source = kwargs.get('source')
        self.body = kwargs.get('body')
        self.tags = str(kwargs.get('tags', '')).split('|')
        self.categories = str(kwargs.get('categories', '')).split('|')
        self.upvotes = kwargs.get('upvotes')
        self.downvotes = kwargs.get('downvotes')
        self.lang = kwargs.get('lang')
        self.source_info = kwargs.get('source_info', '').replace("'", '"')
        self.source_info = NewsItem.Source(**json.loads(self.source_info))


class Coin:
    algorithm: Str
    built_on: Str
    block_number: Str
    block_reward: int
    block_time: int
    coin_name: Str
    content_created_on: int
    full_name: Str
    fully_premined: int
    id: int
    image_url: Str
    is_trading: bool
    name: Str
    net_hashes_per_second: int
    pre_mined_value: Str
    proof_type: Str
    smart_contract_address: Str
    sort_order: int
    sponsored: bool
    symbol: Str
    total_coins_mined: int
    total_coins_free_float: int
    total_coin_supply: int
    url: Str

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, type_parser(v))

    def __setattr__(self, key, value):
        if snake_case(key) in type(self).__annotations__:
            object.__setattr__(self, snake_case(key), value)
        else:
            raise AttributeError()

    def __getattribute__(self, item):
        if snake_case(item) in type(self).__dict__.keys():
            value = object.__getattribute__(self, snake_case(item))
            return value
        else:
            return object.__getattribute__(self, item)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str(self.name)


class Feed(NewsBase):

    def __init__(self, **kwargs):
        self.image = kwargs.get('image')
        self.id = kwargs.get('key')
        self.lang = kwargs.get('lang')
        self.name = kwargs.get('name')


class Category(NewsBase):

    def __init__(self, **kwargs):
        self.name = kwargs.get('categoryName')
        self.excluded_phrases = kwargs.get('excludedPhrases', [])
        self.included_phrases = kwargs.get('includedPhrases', [])
        self.words = kwargs.get('wordsAssociatedWithCategory', [])


class Feeds(UserList):

    def __init__(self, feeds):
        if isinstance(feeds, Dict):
            feeds = feeds.get('Feeds', [])
        super().__init__([Feed(**feed) for feed in feeds or []])

    def by_lang(self, lang):
        return Feeds([d for d in self.data if d.lang.lower() == lang.lower()])

    def by_id(self, feeds_id):
        for feed in self.data:
            if feed.id == feeds_id:
                return feed

    def __str__(self):
        return f'[{", ".join([d.name for d in self.data])}]'

    def __repr__(self):
        return f'{type(self).__name__}{[d.name for d in self.data]}'


class Categories(UserList):

    def __init__(self, categories):
        if isinstance(categories, Dict):
            categories = categories.get('Categories', [])
        super().__init__([Category(**cat) for cat in categories or []])

    def __str__(self):
        return f'[{[d.name for d in self.data]}]'

    def __repr__(self):
        return f'{type(self).__name__}{[d.name for d in self.data]}'
