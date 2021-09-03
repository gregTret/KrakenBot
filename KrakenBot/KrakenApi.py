import requests
import time
import time
import urllib.parse
import hashlib
import hmac
import base64

class KrakenApiRequests:
    def KrakenStatus():
        fail=1
        while (fail==1):
            try:    
                resp = requests.get('https://api.kraken.com/0/public/SystemStatus')
                res=(resp.json()['result']['status'])
                fail=0
            except:
                print ("Failed to get Kraken Status, trying again")
                fail=1
                pass
            time.sleep(5)
        if (res=="online"):
            return 0
        elif (res=="post_only"):
            return 1
        elif (res=="cancel_only"):    
            return 2
        else:
            return 3

    def getCurrentPrice(selection,dataToReturn,currencyPair):
        data=[]
        alt=[]
        url="https://api.kraken.com/0/public/OHLC?pair="+str(currencyPair)+"&interval="+str(selection)
        fail=1
        while (fail==1):
            try:
                resp = requests.get(url) 
                fail=0
            except:
                print ("Failed to get Data, trying again")
                fail=1
                pass 
            time.sleep(5)
        nickname= (str(resp.json()['result'])).split('\'')
        for x in (resp.json()['result'][nickname[1]]):
            data.append(x)
        if (dataToReturn=='all'):
            return data
        elif (dataToReturn=='high'):
            for x in range (len(data)):
                alt.append(float(data[x][2]))
            return alt
        elif (dataToReturn=='low'):
            for x in range (len(data)):
                alt.append(float(data[x][3]))
            return alt
        elif (dataToReturn=='average'):
            for x in range (len(data)):
                alt.append((float(data[x][2])+float(data[x][3]))/2)
            return alt
        elif (dataToReturn=='highAndLow'):
            for x in range (len(data)):
                temp=[]
                temp.append(float(data[x][2]))
                temp.append(float(data[x][3]))
                alt.append(temp)
            return alt

    def get_kraken_signature(urlpath, data, secret):
        postdata = urllib.parse.urlencode(data)
        encoded = (str(data['nonce']) + postdata).encode()
        message = urlpath.encode() + hashlib.sha256(encoded).digest()
        mac = hmac.new(base64.b64decode(secret), message, hashlib.sha512)
        sigdigest = base64.b64encode(mac.digest())
        return sigdigest.decode()

    def kraken_request(uri_path, data, api_key, api_sec, api_url):
        headers = {}
        headers['API-Key'] = api_key
        headers['API-Sign'] = KrakenApiRequests.get_kraken_signature(uri_path, data, api_sec)             
        req = requests.post((api_url + uri_path), headers=headers, data=data)
        return req

    def MarketBuy(apiKey,apiKeyPrivate,amount,cryptoPair):
        api_url = "https://api.kraken.com"
        api_key = apiKey
        api_sec = apiKeyPrivate
        resp = KrakenApiRequests.kraken_request('/0/private/AddOrder', {
            "nonce": str(int(1000*time.time())),
            "ordertype": "market",
            "type": "buy",
            "volume": amount,
            "pair": cryptoPair
        }, api_key, api_sec, api_url)
        print(resp.json())

    def LimitSell(apiKey,apiKeyPrivate,amount,cryptoPair,minPrice):
        api_url = "https://api.kraken.com"
        api_key = apiKey
        api_sec = apiKeyPrivate
        resp = KrakenApiRequests.kraken_request('/0/private/AddOrder', {
            "nonce": str(int(1000*time.time())),
            "ordertype": "limit",
            "type": "sell",
            "volume": amount,
            "pair": cryptoPair,
            "price": minPrice
        }, api_key, api_sec,api_url)
        print(resp.json())

