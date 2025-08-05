import config
import requests
import json

def test_rpc_connection():
    headers = {"content-type": "text/plain"}
    data = json.dumps({"id": config.rid, "method": "getblockchaininfo", "params": []})
    
    print("Making RPC call to:", config.endpoint)
    
    try:
        response = requests.post(config.endpoint, headers=headers, data=data, timeout=10)
        print("Response status code:", response.status_code)
        print("Response:", response.json())
        return response.json()
    except Exception as e:
        print("Error:", str(e))
        return None

if __name__ == "__main__":
    test_rpc_connection()