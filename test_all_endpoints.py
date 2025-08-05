import requests
import json

def test_all_endpoints():
    base_url = "http://localhost:1234"
    
    # Test all endpoints
    endpoints = [
        "/info",
        "/supply",
        "/getprice",
        "/fee",
        "/mempool",
        "/stats",
        "/height/1",
        "/block/f682cda177894276279c9c58a894b711e86f238c856daa8f35d5dde85502cd08",
        "/header/f682cda177894276279c9c58a894b711e86f238c856daa8f35d5dde85502cd08",
        "/range/100?offset=3",
        "/transaction/9fe85d15029318fb53c9b1d891fae5ebff3af8b79e90a72ef0e768ac8cd7dba0",
        "/balance/XXXXXXXXXXXXXXXXXXXXXXXXXXXXarcLhe",
        "/mempool/XXXXXXXXXXXXXXXXXXXXXXXXXXXXarcLhe",
        "/unspent/XXXXXXXXXXXXXXXXXXXXXXXXXXXXarcLhe?amount=1",
        "/history/XXXXXXXXXXXXXXXXXXXXXXXXXXXXarcLhe",
        "/decode/0200000001d253f16a2568c978af216b394fd0cf324f577392cfa3d6440948417c18deadb4000000006a47304402201bf1e8fb97941640c1eec7ddd7c7ae456ffcd842f18a5868948340bfa3eae03d0220632f97d2db40a2fc048fff461cd83316d83a6c0f045db8960c4bc86ab0f02945012103d4780c3dcd9484d0231d22ee45d5fdc35d89c7acdb759ca663b89925136c9ab7fdffffff02ecd6bb956b4a35001976a914a15abdff0b24eb0d7b6d6ce4644fe78f756fcd0488ac0080e03779c3110017a914dd54992549a9b3dd2abc0e51fa082205e96b072087079c1100"
    ]
    
    print("Testing all API endpoints:")
    for endpoint in endpoints:
        try:
            url = base_url + endpoint
            print(f"\nTesting {url}...")
            response = requests.get(url, timeout=10)
            print(f"  Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    # Check if there's an error in the response
                    if isinstance(data, dict) and data.get("error"):
                        print(f"  Error: {data['error']}")
                    else:
                        print(f"  Success: {str(data)[:100]}...")
                except:
                    print(f"  Response: {response.text[:100]}...")
            else:
                print(f"  Error: {response.text}")
        except Exception as e:
            print(f"  Exception: {str(e)}")
    
    # Test POST endpoint
    try:
        print(f"\nTesting POST /broadcast...")
        url = base_url + "/broadcast"
        response = requests.post(url, data={"raw": "test"}, timeout=10)
        print(f"  Status: {response.status_code}")
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"  Response: {str(data)[:100]}...")
            except:
                print(f"  Response: {response.text[:100]}...")
        else:
            print(f"  Error: {response.text}")
    except Exception as e:
        print(f"  Exception: {str(e)}")

if __name__ == "__main__":
    test_all_endpoints()