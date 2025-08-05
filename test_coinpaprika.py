import requests
import json

def test_coinpaprika():
    ticker = "ROD"
    coin_name = "spacexpanse"
    
    try:
        # Test the Coinpaprika API call
        url = f"https://api.coinpaprika.com/v1/tickers/{ticker.lower()}-{coin_name}"
        print(f"Calling URL: {url}")
        
        response = requests.get(url, timeout=10)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {response.headers}")
        
        if response.status_code == 200:
            price_data = response.json()
            print("Response data:")
            print(json.dumps(price_data, indent=2))
            
            # Check if we have the expected data
            if price_data and not price_data.get('error'):
                quotes = price_data.get("quotes", {})
                usd_data = quotes.get("USD", {})
                usd_price = float(usd_data.get("price", 0))
                print(f"USD price: {usd_price}")
            else:
                print("Error in response data")
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Exception occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_coinpaprika()