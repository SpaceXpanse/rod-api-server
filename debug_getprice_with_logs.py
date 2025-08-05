import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

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

def debug_getprice():
    btc = 0.0
    usd = 0.0
    msg = "Error"
    try:
        print("Making request to Coinpaprika API...")
        # Use only Coinpaprika API with correct ticker
        url = "https://api.coinpaprika.com/v1/tickers/rod-spacexpanse"
        print(f"URL: {url}")
        response = requests.get(url, timeout=10)
        print(f"Response status: {response.status_code}")
        price_data = response.json()
        print(f"Price data: {price_data}")
        
        if price_data and not price_data.get('error'):
            print("No error in price data")
            quotes = price_data.get("quotes", {})
            print(f"Quotes: {quotes}")
            usd_data = quotes.get("USD", {})
            print(f"USD data: {usd_data}")
            # BTC price is not available in the response, so we'll set it to 0
            btc = 0.0
            usd = float(usd_data.get("price", 0))
            print(f"BTC: {btc}, USD: {usd}")
            msg = "Active"
            
        result = {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
        print(f"Final result: {result}")
        return result
    except Exception as e:
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return {
            "price_btc": "0.00000000",
            "price_usd": "0.00000000",
            "status": "Error"
        }

if __name__ == "__main__":
    result = debug_getprice()
    print(f"Result: {result}")