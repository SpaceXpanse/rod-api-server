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
    
    block_reward = 800.0
    halving_interval = 1054080
    total_supply = 0.0
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
    
    return {
        "halvings": halvings,
        "supply": satoshis(total_supply),
        "total/max supply": "4,615,066,365 ROD coins"
    }

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def amount(value):
    return round(value / math.pow(10, 8), 8)

def getprice():
    import logging
    ticker = "ROD"
    coin_name = "spacexpanse"
    setactive = "Active"
    btc = 0.0
    usd = 0.0
    msg = "Error"
    try:
        price = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids="+coin_name+"&vs_currencies=usd,btc", timeout=10, verify=False).json()
        price_v2 = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+coin_name, timeout=10, verify=False).json()
        
        price2 = requests.get(f"https://api.coinpaprika.com/v1/ticker/"+ticker+"-"+coin_name, timeout=10, verify=False).json()
        price2_v2 = requests.get(f"https://api.coinpaprika.com/v1/tickers/"+ticker+"-"+coin_name, timeout=10, verify=False).json()
            
        if len(price)>0 and len(price2)>0 and price2_v2.get('error', '')!="id not found":
            cg_lastupdate = price_v2[0].get('last_updated', '')
            if price2_v2.get('error'):
                cp_lastupdate = '1000-07-19 17:31:00'
            else:
                cp_lastupdate = price2_v2.get('last_updated', '')
                
            format_data = "%Y-%m-%d %H:%M:%S"
            
            print('cp_lastupdate'+str(cp_lastupdate),flush=True)
            
            ddate1 = parse(cg_lastupdate) if cg_lastupdate else None
            ddate2 = parse(cp_lastupdate) if cp_lastupdate else None
            
            cp_substr1_date = str(price_v2[0].get('last_updated', '')).split("T") if price_v2[0].get('last_updated') else ['']
            cp_substr1_time = str(cp_substr1_date[1]).split(".") if len(cp_substr1_date) > 1 else ['']
            
            cp_comb_dt = cp_substr1_date[0] + " " + cp_substr1_time[0] if cp_substr1_date and cp_substr1_time else ''
            try:
                cp_comb_cd = datetime.strptime(cp_comb_dt, format_data) if cp_comb_dt else None
            except:
                cp_comb_cd = None
            
            try:
                dt2 = (datetime.fromtimestamp(int(price2.get('last_updated', 0))) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
                dt2_cd = datetime.strptime(dt2, format_data)
            except:
                dt2_cd = None
            
            if cp_comb_cd and dt2_cd and cp_comb_cd > dt2_cd:
                btc = float(price[coin_name]['btc'])
                usd = float(price[coin_name]['usd'])
                msg = setactive
            else:
                btc = float(price2.get("price_btc", 0))
                usd = float(price2.get("price_usd", 0))
                msg = setactive
        elif len(price)>0:
            print('condition 2')
            btc = float(price[coin_name].get('btc', 0))
            usd = float(price[coin_name].get('usd', 0))
            msg = setactive
        elif len(price2)>0:
            print('condition 3')
            btc = float(price2[0].get("price_btc", 0)) if isinstance(price2, list) else float(price2.get("price_btc", 0))
            usd = float(price2[0].get("price_usd", 0)) if isinstance(price2, list) else float(price2.get("price_usd", 0))
            msg = setactive
        else:
             msg = "Error market cap connection"
        return {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
    except Exception as e:
        print(f"Error in getprice: {str(e)}")
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
        setactive = "Active"

        price = requests.get(f"http://cmcdata.widecoin.org?val=coingecko",verify=False, timeout=10).json()
        price2 = requests.get(f"http://cmcdata.widecoin.org?val=coinparika").json()
    
        if len(price)>0:
            btc = float(price[coin_name].get('btc', 0))
            usd = float(price[coin_name].get('usd', 0))
            msg = setactive
        elif len(price2)>0:
            btc = float(price2.get("price_btc", 0))
            usd = float(price2.get("price_usd", 0))
            msg = setactive
        else:
            msg = "Error market cap connection"
        return {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
    except Exception as e:
        print(f"Error in getprice_back: {str(e)}")
        return {
            "price_btc": "0.00000000",
            "price_usd": "0.00000000",
            "status": "Error"
        }

