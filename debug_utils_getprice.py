import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import requests
import config

def debug_getprice():
    btc = 0.0
    usd = 0.0
    msg = "Error"
    try:
        # Use only Coinpaprika API with correct ticker
        url = "https://api.coinpaprika.com/v1/tickers/rod-spacexpanse"
        print(f"Making request to: {url}")
        response = requests.get(url, timeout=10)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        price_data = response.json()
        print(f"Price data: {price_data}")
        
        if price_data and not price_data.get('error'):
            quotes = price_data.get("quotes", {})
            print(f"Quotes: {quotes}")
            usd_data = quotes.get("USD", {})
            print(f"USD data: {usd_data}")
            # BTC price is not available in the response, so we'll set it to 0
            btc = 0.0
            usd = float(usd_data.get("price", 0))
            msg = "Active"
            
        result = {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
        print(f"Result: {result}")
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
    debug_getprice()