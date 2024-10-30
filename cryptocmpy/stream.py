# -*- coding: utf-8 -*-
"""cryptocmpy
  stream module.

  - Author:
  - License:
  - Created:    09-12-2018
  - Modified:   09-12-2018
"""

# !/usr/bin/env python
# coding=utf-8
import json
import logging
import ssl
from pprint import pprint

import requests
import simplejson
import websocket
from events import Events
from six.moves.urllib.parse import urlencode

logging.basicConfig()


class Request(object):
    def __init__(self, api):
        self.api = api

    def _is_wapi(self, path):
        return path.endswith('.html')

    def _get_base_path(self, path):
        return self.api.wapi_base_path if self._is_wapi(path) else self.api.base_path

    def _full_url(self, path):
        return "%s://%s%s%s" % (self.api.protocol,
                                self.api.host,
                                self._get_base_path(path),
                                path)

    def _full_url_with_params(self, path, params):
        return (self._full_url(path) +
                self._full_query_with_params(params))

    def _full_query_with_params(self, params):
        signature = params.pop("signature", None)
        params = ("?" + urlencode(params)) if params else ""
        if signature is not None:
            params = params + "&signature=" + signature
        return params

    def _post_body(self, params):
        signature = params.pop("signature", None)
        body = list(params.items())
        if signature is not None:
            body = body + [("signature", signature)]
        return body

    def prepare_request(self, method, path, params):
        url = body = None
        headers = {}

        if method == "GET" or self._is_wapi(path):
            url = self._full_url_with_params(path, params)
        else:
            url = self._full_url(path)
            body = self._post_body(params)

        return url, method, body, headers

    def make_request(self, url, method="GET", body=None, headers=None):
        headers = headers or {}
        if not 'User-Agent' in headers:
            headers.update({"User-Agent": "%s Python Client" % self.api.api_name})
        if method == "GET":
            return requests.get(url, headers=headers, timeout=60)
        elif method == "POST":
            return requests.post(url, data=body, headers=headers, timeout=60)
        elif method == "DELETE":
            return requests.delete(url, data=body, headers=headers, timeout=60)
        elif method == "PUT":
            return requests.put(url, data=body, headers=headers, timeout=60)


class WebSocket(Events):
    __events__ = ['callback']

    def __init__(self, api, callback=None):
        self.api = api
        self.callback += callback

    def _full_url(self, path):
        return "%s://%s:%s%s%s" % (self.api.protocol,
                                   self.api.host,
                                   self.api.port,
                                   self.api.base_path,
                                   path)

    def _on_message(self, ws, message):
        data = simplejson.loads(message)
        self.callback(data)

    def _on_error(self, ws, error):
        raise Exception(error)

    def prepare_request(self, path):
        url = self._full_url(path)

        return url

    def run_forever(self, url):
        self.ws = websocket.WebSocketApp(url,
                                         on_message=self._on_message,
                                         on_error=self._on_error)
        self.ws.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE})


if __name__ == '__main__':
    """
    var currentPrice = {};
	var socket = io.connect('https://streamer.cryptocompare.com/');
	//Format: {SubscriptionId}~{ExchangeName}~{FromSymbol}~{ToSymbol}
	//Use SubscriptionId 0 for TRADE, 2 for CURRENT, 5 for CURRENTAGG eg use key '5~CCCAGG~BTC~USD' to get aggregated data from the CCCAGG exchange 
	//Full Volume Format: 11~{FromSymbol} eg use '11~BTC' to get the full volume of BTC against all coin pairs
	//For aggregate quote updates use CCCAGG ags market
	var subscription = ['5~CCCAGG~BTC~USD', '5~CCCAGG~ETH~USD', '5~CCCAGG~BTS~USD', '5~CCCAGG~AMIS~ETH', '5~CCCAGG~EOS~USD', '5~EtherDelta~AMIS~ETH', '11~BTC', '11~ETH', '11~AMIS', '11~EOS', '11~BTS'];
	socket.emit('SubAdd', { subs: subscription });
    """
    resp = '{"Message":"Success","Type":100,"SponsoredData":[{"CoinInfo":{"Id":"925695","Name":"CRYP","FullName":"CrypticCoin","Internal":"CRYP","ImageUrl":"/media/34478470/cryp.png","Url":"/coins/cryp/overview","Algorithm":"Equihash","ProofType":"PoW","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":150,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"multiply","ConversionSymbol":"ETH","CurrencyFrom":"CRYP","CurrencyTo":"USD","Market":"CCCAGG","Supply":4235111504,"TotalVolume24H":250098,"SubBase":"5~","SubsNeeded":["5~CCCAGG~CRYP~ETH","5~CCCAGG~ETH~USD"],"RAW":["5~CCCAGG~CRYP~ETH~4~0.0000192~1544300339~402~0.0077184~15443003390001~0~0~54031~0.86349896~0.0000192~0.0000192~0.0000192~0.0000125~0.0000192~0.0000125~BitMart~7ffe9","5~CCCAGG~ETH~USD~4~92.18~1544321213~5.7612~522.425616~79292315~66289.32459433934~6101340.02851251~1156244.4075028403~104262947.6211358~91.44~92.8~91.23~95.4~96.63~84.74~Bitstamp~7ffe9"]}}],"Data":[{"CoinInfo":{"Id":"899553","Name":"QKC","FullName":"QuarkChain","Internal":"QKC","ImageUrl":"/media/33434307/qkc.jpg","Url":"/coins/qkc/overview","Algorithm":"N/A","ProofType":"N/A","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":0,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"multiply","ConversionSymbol":"BTC","CurrencyFrom":"QKC","CurrencyTo":"USD","Market":"CCCAGG","Supply":10000000000,"TotalVolume24H":88943915.67237386,"SubBase":"5~","SubsNeeded":["5~CCCAGG~QKC~BTC","5~CCCAGG~BTC~USD"],"RAW":["5~CCCAGG~QKC~BTC~2~0.00001241~1544321045~1856~0.023032959999999998~3693428~1835447.6359~22.726718932485024~72508948.7757~892.0942945021843~0.00001232~0.00001249~0.00001224~0.0000122~0.00001273~0.00001169~Binance~7ffe9","5~CCCAGG~BTC~USD~4~3472.49~1544321223~0.025~88~321781349~6657.23171709282~23072214.142127007~96019.43217157976~329544549.2833817~3461.07~3497.81~3450.96~3469.21~3648.45~3295.13~Bitfinex~7ffe9"]}},{"CoinInfo":{"Id":"5324","Name":"ETC","FullName":"Ethereum Classic","Internal":"ETC","ImageUrl":"/media/33752295/etc_new.png","Url":"/coins/etc/overview","Algorithm":"Ethash","ProofType":"PoW","NetHashesPerSecond":10676455206117,"BlockNumber":0,"BlockTime":18,"BlockReward":4,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"direct","ConversionSymbol":"","CurrencyFrom":"ETC","CurrencyTo":"USD","Market":"CCCAGG","Supply":106621116,"TotalVolume24H":31637832.880176764,"SubBase":"5~","SubsNeeded":["5~CCCAGG~ETC~USD"],"RAW":["5~CCCAGG~ETC~USD~4~3.92~1544321202~8.57591936~32.845771148800004~1198607~122707.18759963007~481633.7124224692~1745852.01144241~6637624.834149298~3.86~3.96~3.84~3.93~4.11~3.54~Coinbase~7ffe9"]}},{"CoinInfo":{"Id":"41192","Name":"MKR","FullName":"Maker","Internal":"MKR","ImageUrl":"/media/1382296/mkr.png","Url":"/coins/mkr/overview","Algorithm":"N/A","ProofType":"N/A","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":0,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"multiply","ConversionSymbol":"ETH","CurrencyFrom":"MKR","CurrencyTo":"USD","Market":"CCCAGG","Supply":1000000,"TotalVolume24H":251.4925336099742,"SubBase":"5~","SubsNeeded":["5~CCCAGG~MKR~ETH","5~CCCAGG~ETH~USD"],"RAW":["5~CCCAGG~MKR~ETH~4~3.76~1544321166~0.01864~0.068036~15443211660001~1.1855931800000004~4.456786989583001~71.5357918~264.727296976391~3.74~3.8~3.73~3.6~4.07~3.6~BitMart~7ffe9","5~CCCAGG~ETH~USD~4~92.18~1544321213~5.7612~522.425616~79292315~66289.32459433934~6101340.02851251~1156244.4075028403~104262947.6211358~91.44~92.8~91.23~95.4~96.63~84.74~Bitstamp~7ffe9"]}},{"CoinInfo":{"Id":"808414","Name":"ONT","FullName":"Ontology","Internal":"ONT","ImageUrl":"/media/30001663/ont.jpg","Url":"/coins/ont/overview","Algorithm":"N/A","ProofType":"PoS","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":0,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"multiply","ConversionSymbol":"BTC","CurrencyFrom":"ONT","CurrencyTo":"USD","Market":"CCCAGG","Supply":597000000,"TotalVolume24H":12602538.446397293,"SubBase":"5~","SubsNeeded":["5~CCCAGG~ONT~BTC","5~CCCAGG~BTC~USD"],"RAW":["5~CCCAGG~ONT~BTC~2~0.0001603~1544321198~0.5149~0.00008269294~3.150557753218847e+21~300713.88889999996~48.230378655623035~3511470.050580701~561.658526562526~0.0001606~0.0001628~0.0001585~0.0001677~0.0001692~0.0001562~HuobiPro~7ffe9","5~CCCAGG~BTC~USD~4~3472.49~1544321223~0.025~88~321781349~6657.23171709282~23072214.142127007~96019.43217157976~329544549.2833817~3461.07~3497.81~3450.96~3469.21~3648.45~3295.13~Bitfinex~7ffe9"]}},{"CoinInfo":{"Id":"186277","Name":"ZRX","FullName":"0x","Internal":"ZRX","ImageUrl":"/media/1383799/zrx.png","Url":"/coins/zrx/overview","Algorithm":"N/A","ProofType":"N/A","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":0,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"direct","ConversionSymbol":"","CurrencyFrom":"ZRX","CurrencyTo":"USD","Market":"CCCAGG","Supply":1000000000,"TotalVolume24H":22383550.0317591,"SubBase":"5~","SubsNeeded":["5~CCCAGG~ZRX~USD"],"RAW":["5~CCCAGG~ZRX~USD~2~0.3209~1544321210~400.06241~127.84954461334002~653896~265685.27802439~84787.42136031465~4804910.665481832~1547908.3953761067~0.3164~0.3229~0.314~0.3263~0.3548~0.2965~Coinbase~7ffe9"]}},{"CoinInfo":{"Id":"24854","Name":"ZEC","FullName":"ZCash","Internal":"ZEC","ImageUrl":"/media/351360/zec.png","Url":"/coins/zec/overview","Algorithm":"Equihash","ProofType":"PoW","NetHashesPerSecond":2298303854,"BlockNumber":442690,"BlockTime":150,"BlockReward":10,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"direct","ConversionSymbol":"","CurrencyFrom":"ZEC","CurrencyTo":"USD","Market":"CCCAGG","Supply":5408631.25,"TotalVolume24H":2037036.5878676793,"SubBase":"5~","SubsNeeded":["5~CCCAGG~ZEC~USD"],"RAW":["5~CCCAGG~ZEC~USD~2~58.56~1544321165~0.135~7.68015~5099002300~1589.828537250001~92188.67942631632~38109.17697917001~2206995.4800954163~57.57~58.99~57.2~60.13~61.52~53.84~Gemini~7ffe9"]}},{"CoinInfo":{"Id":"177918","Name":"KIN","FullName":"Kin","Internal":"KIN","ImageUrl":"/media/1383731/kin.png","Url":"/coins/kin/overview","Algorithm":"N/A","ProofType":"N/A","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":0,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"multiply","ConversionSymbol":"ETH","CurrencyFrom":"KIN","CurrencyTo":"USD","Market":"CCCAGG","Supply":10000000000000,"TotalVolume24H":2286207831.765236,"SubBase":"5~","SubsNeeded":["5~CCCAGG~KIN~ETH","5~CCCAGG~ETH~USD"],"RAW":["5~CCCAGG~KIN~ETH~4~3e-7~1544321168~800000~0.2416~413879359~84237693.4846058~25.78428411099625~2191014872.771424~654.4975878091137~3e-7~3.1e-7~3e-7~3.1e-7~3.1e-7~2.9e-7~HitBTC~7ffe9","5~CCCAGG~ETH~USD~4~92.18~1544321213~5.7612~522.425616~79292315~66289.32459433934~6101340.02851251~1156244.4075028403~104262947.6211358~91.44~92.8~91.23~95.4~96.63~84.74~Bitstamp~7ffe9"]}},{"CoinInfo":{"Id":"4432","Name":"DOGE","FullName":"Dogecoin","Internal":"DOGE","ImageUrl":"/media/19684/doge.png","Url":"/coins/doge/overview","Algorithm":"Scrypt","ProofType":"PoW","NetHashesPerSecond":0,"BlockNumber":2507501,"BlockTime":0,"BlockReward":0.0000217982700892857,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"direct","ConversionSymbol":"","CurrencyFrom":"DOGE","CurrencyTo":"USD","Market":"CCCAGG","Supply":117320780908.627,"TotalVolume24H":2476067790.095708,"SubBase":"5~","SubsNeeded":["5~CCCAGG~DOGE~USD"],"RAW":["5~CCCAGG~DOGE~USD~4~0.002059~1544320756~1576.13~3.2456299412000003~881393151~1648349.2590071496~3436.5754632987614~12992703.949136639~27497.25990458818~0.002085~0.00211~0.002029~0.002144~0.002167~0.002029~LiveCoin~7ffe9"]}},{"CoinInfo":{"Id":"309621","Name":"LINK","FullName":"ChainLink","Internal":"LINK","ImageUrl":"/media/12318078/link.png","Url":"/coins/link/overview","Algorithm":"N/A","ProofType":"N/A","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":0,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"multiply","ConversionSymbol":"BTC","CurrencyFrom":"LINK","CurrencyTo":"USD","Market":"CCCAGG","Supply":1000000000,"TotalVolume24H":8234694.2510482455,"SubBase":"5~","SubsNeeded":["5~CCCAGG~LINK~BTC","5~CCCAGG~BTC~USD"],"RAW":["5~CCCAGG~LINK~BTC~2~0.00006515~1544321191~177~0.01153155~4211770~390032.1669999996~25.520201515819974~6769969.299000001~452.9149612988601~0.00006554~0.00006599~0.000065~0.00006444~0.00007253~0.00006187~Binance~7ffe9","5~CCCAGG~BTC~USD~4~3472.49~1544321223~0.025~88~321781349~6657.23171709282~23072214.142127007~96019.43217157976~329544549.2833817~3461.07~3497.81~3450.96~3469.21~3648.45~3295.13~Bitfinex~7ffe9"]}},{"CoinInfo":{"Id":"236131","Name":"VET","FullName":"Vechain","Internal":"VET","ImageUrl":"/media/12318129/ven.png","Url":"/coins/vet/overview","Algorithm":"N/A","ProofType":"N/A","NetHashesPerSecond":0,"BlockNumber":0,"BlockTime":0,"BlockReward":0,"Type":1,"DocumentType":"Webpagecoinp"},"ConversionInfo":{"Conversion":"multiply","ConversionSymbol":"BTC","CurrencyFrom":"VET","CurrencyTo":"USD","Market":"CCCAGG","Supply":55454734800,"TotalVolume24H":1071201822.7902359,"SubBase":"5~","SubsNeeded":["5~CCCAGG~VET~BTC","5~CCCAGG~BTC~USD"],"RAW":["5~CCCAGG~VET~BTC~4~0.00000113~1544321186~19999~0.0224088795~3.150556268318847e+21~30597749.88641545~34.33085387963225~485084510.8370318~551.7678869016247~0.00000113~0.00000113~0.00000112~0.00000116~0.00000118~0.00000111~HuobiPro~7ffe9","5~CCCAGG~BTC~USD~4~3472.49~1544321223~0.025~88~321781349~6657.23171709282~23072214.142127007~96019.43217157976~329544549.2833817~3461.07~3497.81~3450.96~3469.21~3648.45~3295.13~Bitfinex~7ffe9"]}}],"RateLimit":{},"HasWarning":false}'

    data = json.loads(resp)
    pprint(data)


    def callback(*args, **kwargs):
        print(len(args))
        print(len(kwargs))


    subscription = ['5~CCCAGG~BTC~USD', '5~CCCAGG~ETH~USD', '5~CCCAGG~BTS~USD', '5~CCCAGG~AMIS~ETH', '5~CCCAGG~EOS~USD',
                    '5~EtherDelta~AMIS~ETH', '11~BTC', '11~ETH', '11~AMIS', '11~EOS', '11~BTS']
    ws = WebSocket('https://streamer.cryptocompare.com/', callback)
    ws.prepare_request()
