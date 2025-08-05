import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import in the same order as the server
import eventlet
eventlet.monkey_patch()

import requests
import config
import math
import json

def getprice():
    btc = 0.0
    usd = 0.0
    msg = "Error"
    try:
        # Use only Coinpaprika API with correct ticker
        url = "https://api.coinpaprika.com/v1/tickers/rod-spacexpanse"
        # Disable SSL verification to avoid recursion issues with eventlet
        response = requests.get(url, timeout=10, verify=False)
        price_data = response.json()
        
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
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return {
            "price_btc": "0.00000000",
            "price_usd": "0.00000000",
            "status": "Error"
        }

if __name__ == "__main__":
    result = getprice()
    print(f"Result: {result}")