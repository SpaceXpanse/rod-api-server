import requests
import json

def test_coinpaprika_api():
    """Direct test of Coinpaprika API without any Flask or app context"""
    print("Testing Coinpaprika API directly...")
    
    # Test the exact URL that should work
    url = "https://api.coinpaprika.com/v1/tickers/rod-spacexpanse"
    print(f"Calling URL: {url}")
    
    try:
        response = requests.get(url, timeout=10)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data keys: {list(data.keys())}")
            print(f"Symbol: {data.get('symbol', 'N/A')}")
            print(f"Name: {data.get('name', 'N/A')}")
            
            # Check quotes data
            quotes = data.get('quotes', {})
            print(f"Quotes keys: {list(quotes.keys())}")
            
            if 'USD' in quotes:
                usd_data = quotes['USD']
                print(f"USD price: {usd_data.get('price', 'N/A')}")
                result = {
                    "price_btc": "0.00000000",  # BTC not available in response
                    "price_usd": f"%.8f" % float(usd_data.get('price', 0)),
                    "status": "Active"
                }
                print(f"Final result: {result}")
                return result
            else:
                print("No USD data in quotes")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        import traceback
        traceback.print_exc()
    
    # Error result
    result = {
        "price_btc": "0.00000000",
        "price_usd": "0.00000000",
        "status": "Error"
    }
    print(f"Error result: {result}")
    return result

if __name__ == "__main__":
    test_coinpaprika_api()