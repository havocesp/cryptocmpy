# -*- coding:utf-8 -*-
"""
Utils module.
"""
import pprint
import typing
import urllib.request
from http.client import HTTPResponse
from http.client import responses

responses


class Header(typing.ItemsView):
    CONTENT_TYPE = 'Content-Type'

    def __init__(self, header, content):
        self.type = header
        self.content = content


if __name__ == '__main__':
    url = 'https://cryptopia.co.nz/api/GetMarket/BTC_USDT/1'

    data = urllib.request.urlopen(url)  # type: HTTPResponse

    pprint.pprint(data.getheaders())
    if data.getcode() == 200:
        headers = data.getheaders()
        content_type = headers.get(Header)
        lines = data.readlines()
        if lines and len(lines):
            raw_json = lines.pop(0)
            print()
