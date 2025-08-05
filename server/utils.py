import config
import math
import json
import datetime
import requests
from dateutil.parser import parse
from datetime import datetime, timedelta
from dateutil import parser
from urllib.parse import urlparse
from urllib.parse import parse_qs
import decimal
import sys


def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid):
    return {"error": error, "id": rid, "result": result}

def make_request(method, params=[]):
    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(config.endpoint, headers=headers, data=data).json()
    except Exception:
        return dead_response()

def reward(height):
    # SpaceXpanse ROD block reward: 800 ROD with halving every 1,054,080 blocks
    halvings = height // 1054080
    if halvings >= 64:
        return 0
    return int(satoshis(800.00000000) // (2 ** halvings))

def reward2(blockHeight):
    # SpaceXpanse ROD block reward: 800 ROD with halving every 1,054,080 blocks
    # 75%/25% distribution (3 neoscrypt-xaya blocks and 1 SHA256d block every 4 blocks)
    # For simplicity, we'll return the average reward per block (800 ROD)
    halvings = blockHeight // 1054080
    if halvings >= 64:
        return 0
    reward = 800.0 / (2 ** halvings)
    return format(reward, '.8f')

def significant(num, signum):
    expo = 10**(int(math.log(num, 10)) - signum + 1)
    return expo * (num // expo)

def supply(height):
    # SpaceXpanse ROD supply calculation
    # 800 ROD block reward with halving every 1,054,080 blocks
    # 75%/25% distribution (3 neoscrypt-xaya blocks and 1 SHA256d block every 4 blocks)
    # Max supply is capped at 4,615,066,365 ROD coins
    # Genesis block premine: 199,999,998 ROD coins
    
    # Add genesis block premine
    premine = 199999998.0
    total_supply = premine
    
    block_reward = 800.0
    halving_interval = 1054080
    remaining_height = height
    halvings = 0
    
    while remaining_height >= halving_interval and halvings < 64:
        # Add supply for this halving period
        total_supply += halving_interval * block_reward
        remaining_height -= halving_interval
        block_reward /= 2.0
        halvings += 1
    
    # Add supply for remaining blocks in current period
    total_supply += remaining_height * block_reward
    
    # Max supply is capped at 4,615,066,365 ROD coins
    max_supply = 4615066365.0
    
    return {
        "halvings": halvings,
        "supply": satoshis(total_supply),
        "total/max supply": satoshis(max_supply)
    }

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def amount(value):
    return round(value / math.pow(10, 8), 8)

def getprice():
    btc = 0.0
    usd = 0.0
    msg = "Error"
    try:
        # Use only Coinpaprika API with correct ticker
        import urllib.request
        import urllib.error
        import json
        
        url = "https://api.coinpaprika.com/v1/tickers/rod-spacexpanse"
        req = urllib.request.Request(url)
        req.add_header('User-Agent', 'Mozilla/5.0')
        
        try:
            response = urllib.request.urlopen(req, timeout=10)
            data = response.read()
            price_data = json.loads(data)
        except urllib.error.URLError as e:
            # Try without SSL verification
            import ssl
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            response = urllib.request.urlopen(req, timeout=10, context=context)
            data = response.read()
            price_data = json.loads(data)
        
        if price_data and not price_data.get('error'):
            quotes = price_data.get("quotes", {})
            usd_data = quotes.get("USD", {})
            # BTC price is not available in the response, so we'll set it to 0
            btc = 0.0
            usd = float(usd_data.get("price", 0))
            msg = "Active"
            
        result = {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
        return result
    except Exception as e:
        return {
            "price_btc": "0.00000000",
            "price_usd": "0.00000000",
            "status": "Error"
        }
        
def getprice_back():
    btc = 0.0
    usd = 0.0
    msg = "Error"
    try:
        ticker = "ROD"
        coin_name = "spacexpanse"

        # Use only Coinpaprika API with correct ticker
        price_data = requests.get(f"https://api.coinpaprika.com/v1/tickers/"+ticker.lower()+"-"+coin_name, timeout=10, verify=False).json()
    
        if price_data and not price_data.get('error'):
            quotes = price_data.get("quotes", {})
            usd_data = quotes.get("USD", {})
            # BTC price is not available in the response, so we'll set it to 0
            btc = 0.0
            usd = float(usd_data.get("price", 0))
            msg = "Active"
        else:
            msg = "Error market cap connection"
        return {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
    except Exception as e:
        return {
            "price_btc": "0.00000000",
            "price_usd": "0.00000000",
            "status": "Error"
        }

