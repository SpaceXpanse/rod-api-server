import requests
import json

def test_api_endpoints():
    # Test the main API endpoints
    base_url = "http://localhost:1234"
    
    # Test endpoints to check
    endpoints = [
        "/info",
        "/supply",
        "/getprice",
        "/fee",
        "/mempool"
    ]
    
    print("Testing API endpoints:")
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"Testing {url}...")
            response = requests.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"  Response: {json.dumps(data, indent=2)[:200]}...")
                except:
                    print(f"  Response: {response.text[:200]}...")
            else:
                print(f"  Error: {response.text}")
        except Exception as e:
            print(f"  Exception: {str(e)}")
        print()

if __name__ == "__main__":
    test_api_endpoints()