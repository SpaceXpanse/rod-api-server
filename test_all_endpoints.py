import requests
import json

base_url = "http://localhost:1234"

endpoints = [
    "/getprice",
    "/price",
    "/info",
    "/supply"
]

print("Testing all endpoints:")
print("=" * 50)

for endpoint in endpoints:
    try:
        response = requests.get(base_url + endpoint)
        data = response.json()
        print(f"{endpoint}:")
        print(f"  Status: {response.status_code}")
        print(f"  Error: {data.get('error')}")
        print(f"  Result: {data.get('result')}")
        print()
    except Exception as e:
        print(f"{endpoint}: ERROR - {e}")
        print()

print("Test completed.")