import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import in the same order as the server
import eventlet
eventlet.monkey_patch()

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