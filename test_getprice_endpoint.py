import requests
import json

def test_getprice_endpoint():
    """Test the getprice endpoint directly with detailed error handling"""
    print("Testing getprice endpoint...")
    
    try:
        response = requests.get("http://localhost:1234/getprice", timeout=10)
        print(f"Response status code: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response data: {data}")
            
            # Check if there's an error in the response
            if data.get("error") is not None:
                print(f"API returned error: {data['error']}")
            else:
                result = data.get("result", {})
                print(f"Result data: {result}")
                return result
        else:
            print(f"HTTP error {response.status_code}: {response.text}")
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        print(f"Response text: {response.text}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
    
    return None

if __name__ == "__main__":
    result = test_getprice_endpoint()
    if result:
        print(f"Success: {result}")
    else:
        print("Failed to get valid response")