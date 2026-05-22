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

RPC_TIMEOUT_SECONDS = getattr(config, "rpc_timeout", 10)
MARKET_TIMEOUT_SECONDS = getattr(config, "market_timeout", 10)

ROD_PRE_RELEASE_BLOCKS = 55560
ROD_PRE_RELEASE_REWARD = 1.0
ROD_STANDARD_REWARD = 800.0
ROD_HALVING_INTERVAL = 1054080
ROD_HALVING_PERIODS = 5
ROD_ANNUAL_INFLATION = 0.03
ROD_POST_HALVING_YEARS = 59
ROD_SECONDS_PER_BLOCK = 30
ROD_BLOCKS_PER_YEAR = int((365 * 24 * 60 * 60) / ROD_SECONDS_PER_BLOCK)
ROD_MAX_SUPPLY = 4615066365


def dead_response(message="Invalid Request", rid=config.rid):
    return {"error": {"code": 404, "message": message}, "id": rid}

def response(result, error=None, rid=config.rid):
    return {"error": error, "id": rid, "result": result}

def make_request(method, params=None):
    if params is None:
        params = []

    headers = {"content-type": "text/plain;"}
    data = json.dumps({"id": config.rid, "method": method, "params": params})

    try:
        return requests.post(
            config.endpoint,
            headers=headers,
            data=data,
            timeout=RPC_TIMEOUT_SECONDS,
        ).json()
    except Exception:
        return dead_response()

def reward(height):
    if height <= 0:
        return 0
    if height <= ROD_PRE_RELEASE_BLOCKS:
        return satoshis(ROD_PRE_RELEASE_REWARD)

    effective_height = height - ROD_PRE_RELEASE_BLOCKS
    halving_index = (effective_height - 1) // ROD_HALVING_INTERVAL

    if halving_index < ROD_HALVING_PERIODS:
        current_reward = ROD_STANDARD_REWARD / (2 ** halving_index)
        return satoshis(current_reward)

    years_after_halving = (effective_height - (ROD_HALVING_INTERVAL * ROD_HALVING_PERIODS)) / ROD_BLOCKS_PER_YEAR
    inflation_multiplier = (1 + ROD_ANNUAL_INFLATION) ** max(0.0, years_after_halving)
    inflationary_reward = (ROD_STANDARD_REWARD / (2 ** ROD_HALVING_PERIODS)) * inflation_multiplier
    return satoshis(inflationary_reward)

def reward2(blockHeight):
    return format(amount(reward(blockHeight)), '.8f')

def significant(num, signum):
    expo = 10**(int(math.log(num, 10)) - signum + 1)
    return expo * (num // expo)

def supply(height):
    if height <= 0:
        return {
            "halvings": 0,
            "supply": 0,
            "total/max supply": satoshis(ROD_MAX_SUPPLY),
            "policy": "spacexpanse-rod",
            "inflation_model": "approximate_3_percent_annual_post_halving",
        }

    total_supply = 0.0
    remaining_blocks = int(height)

    pre_release_blocks = min(remaining_blocks, ROD_PRE_RELEASE_BLOCKS)
    total_supply += pre_release_blocks * ROD_PRE_RELEASE_REWARD
    remaining_blocks -= pre_release_blocks

    completed_halvings = 0
    for halving_index in range(ROD_HALVING_PERIODS):
        if remaining_blocks <= 0:
            break
        phase_blocks = min(remaining_blocks, ROD_HALVING_INTERVAL)
        phase_reward = ROD_STANDARD_REWARD / (2 ** halving_index)
        total_supply += phase_blocks * phase_reward
        remaining_blocks -= phase_blocks
        if phase_blocks == ROD_HALVING_INTERVAL:
            completed_halvings = halving_index + 1

    if remaining_blocks > 0:
        inflationary_base_reward = ROD_STANDARD_REWARD / (2 ** ROD_HALVING_PERIODS)

        for year_index in range(ROD_POST_HALVING_YEARS):
            if remaining_blocks <= 0:
                break
            blocks_this_year = min(remaining_blocks, ROD_BLOCKS_PER_YEAR)
            inflationary_reward = inflationary_base_reward * ((1 + ROD_ANNUAL_INFLATION) ** year_index)
            total_supply += blocks_this_year * inflationary_reward
            remaining_blocks -= blocks_this_year

        if remaining_blocks > 0:
            final_year_reward = inflationary_base_reward * ((1 + ROD_ANNUAL_INFLATION) ** (ROD_POST_HALVING_YEARS - 1))
            total_supply += remaining_blocks * final_year_reward

    return {
        "halvings": int(completed_halvings),
        "supply": satoshis(total_supply),
        "total/max supply": satoshis(ROD_MAX_SUPPLY),
        "policy": "spacexpanse-rod",
        "inflation_model": "approximate_3_percent_annual_post_halving",
    }

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def amount(value):
    return round(value / math.pow(10, 8), 8)

def is_plausible_rod_address(address):
    if not isinstance(address, str):
        return False

    normalized = address.strip()
    if len(normalized) < 26 or len(normalized) > 90:
        return False

    if normalized.startswith("rod1"):
        return True

    return normalized.startswith("R")

def getprice_back():
    import logging
    ticker = "WCN"
    coin_name = "widecoin"
    setactive = "Active"
    price = requests.get(f"https://api.coingecko.com/api/v3/simple/price?ids="+coin_name+"&vs_currencies=usd,btc").json()
    price_v2 = requests.get(f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids="+coin_name).json()
    
    price2 = requests.get(f"https://api.coinpaprika.com/v1/ticker/"+ticker+"-"+coin_name).json()
    price2_v2 = requests.get(f"https://api.coinpaprika.com/v1/tickers/"+ticker+"-"+coin_name).json()
        
    if len(price)>0 and len(price2)>0 and price2_v2['error']!="id not found":
        cg_lastupdate = price_v2[0]['last_updated']
        if len(price2_v2['error'])>0:
            cp_lastupdate = '1000-07-19 17:31:00'
        else:
            cp_lastupdate = price2_v2['last_updated']
            
        format_data = "%Y-%m-%d %H:%M:%S"     
        
        print('cp_lastupdate'+str(cp_lastupdate),flush=True)
        
        ddate1 = parse(cg_lastupdate)
        ddate2 = parse(cp_lastupdate)
        
        cp_substr1_date = str(price_v2[0]['last_updated']).split("T")
        cp_substr1_time = str(cp_substr1_date[1]).split(".")
        
        cp_comb_dt = cp_substr1_date[0] + " " + cp_substr1_time[0]
        cp_comb_cd = datetime.strptime(cp_comb_dt, format_data)
        
        dt2 = (datetime.fromtimestamp(int(price2['last_updated'])) - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M:%S')
        dt2_cd = datetime. strptime(dt2, format_data)
        
        if cp_comb_cd > dt2_cd:
            btc = float(price[coin_name]['btc'])
            usd = float(price[coin_name]['usd'])
            msg = setactive
        else:
            btc = float(price2["price_btc"])
            usd = float(price2["price_usd"])
            msg = setactive
    elif len(price)>0:
        print('condition 2')
        btc = float(price[coin_name]['btc'])
        usd = float(price[coin_name]['usd'])
        msg = setactive
    elif len(price2)>0:
        print('condition 3')
        btc = float(price2["price_btc"])
        usd = float(price2["price_usd"])
        msg = setactive     
    else:
         msg = "Error market cap connection"
    return {
        "price_btc": ('%.8f' % btc),
        "price_usd": ('%.8f' % usd),
        "status": msg
    }
        
def getprice():
    coin_name = "spacexpanse"
    coin_paprika_id = "rod-spacexpanse"

    btc = 0.0
    usd = 0.0
    msg = "Error market cap connection"

    try:
        price = requests.get(
            f"https://api.coingecko.com/api/v3/simple/price?ids={coin_name}&vs_currencies=usd,btc",
            timeout=MARKET_TIMEOUT_SECONDS,
        ).json()
        if isinstance(price, dict) and coin_name in price:
            btc = float(price[coin_name].get("btc", 0) or 0)
            usd = float(price[coin_name].get("usd", 0) or 0)
            msg = "Active"
    except Exception:
        pass

    if msg != "Active":
        try:
            price2 = requests.get(
                f"https://api.coinpaprika.com/v1/tickers/{coin_paprika_id}",
                timeout=MARKET_TIMEOUT_SECONDS,
            ).json()
            if isinstance(price2, dict):
                quotes = price2.get("quotes", {}).get("USD", {})
                usd = float(quotes.get("price", 0) or 0)
                btc = float(price2.get("price_btc", 0) or 0)
                if usd > 0 or btc > 0:
                    msg = "Active"
        except Exception:
            pass

    return {
        "price_btc": ('%.8f' % btc),
        "price_usd": ('%.8f' % usd),
        "status": msg
    }

