import sys
import os
import requests

# Add the server directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

def test_getprice_in_context():
    """Test getprice function in a way that mimics Flask context"""
    print("Testing getprice function in isolated context...")
    
    btc = 0.0
    usd = 0.0
    msg = "Error"
    
    try:
        # Use only Coinpaprika API with correct ticker
        url = "https://api.coinpaprika.com/v1/tickers/rod-spacexpanse"
        print(f"Calling Coinpaprika API: {url}")
        
        # Make the request without any Flask context
        price_data = requests.get(url, timeout=10, verify=False).json()
        print(f"Received data: {type(price_data)}")
        print(f"Data keys: {list(price_data.keys()) if isinstance(price_data, dict) else 'Not a dict'}")
        
        if price_data and not price_data.get('error'):
            quotes = price_data.get("quotes", {})
            print(f"Quotes: {quotes}")
            usd_data = quotes.get("USD", {})
            print(f"USD data: {usd_data}")
            
            # BTC price is not available in the response, so we'll set it to 0
            btc = 0.0
            usd = float(usd_data.get("price", 0))
            msg = "Active"
            print(f"Successfully retrieved prices: BTC={btc}, USD={usd}")
            
        result = {
            "price_btc": ('%.8f' % btc),
            "price_usd": ('%.8f' % usd),
            "status": msg
        }
        print(f"Returning result: {result}")
        return result
    except Exception as e:
        print(f"Error in getprice: {e}")
        import traceback
        traceback.print_exc()
        return {
            "price_btc": "0.00000000",
            "price_usd": "0.00000000",
            "status": "Error"
        }

if __name__ == "__main__":
    result = test_getprice_in_context()
    print(f"Final result: {result}")