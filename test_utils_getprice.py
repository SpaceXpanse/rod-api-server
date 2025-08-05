import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

# Import only what we need to avoid circular imports
import requests
import json

def test_utils_getprice():
    ticker = "ROD"
    coin_name = "spacexpanse"
    btc = 0.0
    usd = 0.0
    msg = "Error"
    try:
        # Use only Coinpaprika API with correct ticker
        url = f"https://api.coinpaprika.com/v1/tickers/{ticker.lower()}-{coin_name}"
        print(f"Calling Coinpaprika API: {url}")
        price_data = requests.get(url, timeout=10).json()
        print(f"Coinpaprika response: {price_data}")
        
        if price_data and not price_data.get('error'):
            quotes = price_data.get("quotes", {})
            usd_data = quotes.get("USD", {})
            # BTC price is not available in the response, so we'll set it to 0
            btc = 0.0
            usd = float(usd_data.get("price", 0))
            msg = "Active"
            print(f"Successfully retrieved prices: BTC={btc}, USD={usd}")
        else:
            msg = "Error market cap connection"
            print(f"Error in Coinpaprika response: {price_data.get('error', 'Unknown error')}")
            
        result = {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
        print(f"Returning result: {result}")
        return result
    except Exception as e:
        print(f"Error in getprice: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "price_btc": "0.00000000",
            "price_usd": "0.00000000",
            "status": "Error"
        }

if __name__ == "__main__":
    result = test_utils_getprice()
    print(f"Final result: {result}")