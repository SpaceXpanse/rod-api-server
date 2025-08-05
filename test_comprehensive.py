import config
import requests
import json
from server import utils

def test_rpc_connection():
    headers = {"content-type": "text/plain"}
    data = json.dumps({"id": config.rid, "method": "getblockchaininfo", "params": []})
    
    print("Making RPC call to:", config.endpoint)
    
    try:
        response = requests.post(config.endpoint, headers=headers, data=data, timeout=10)
        print("Response status code:", response.status_code)
        result = response.json()
        print("Response:", result)
        return result
    except Exception as e:
        print("Error:", str(e))
        return None

def test_reward_functions():
    print("\nTesting reward functions:")
    # Test reward function with current block height
    current_height = 3103718  # From our previous test
    reward_val = utils.reward(current_height)
    reward2_val = utils.reward2(current_height)
    supply_info = utils.supply(current_height)
    
    print(f"Reward at block {current_height}: {reward_val}")
    print(f"Reward2 at block {current_height}: {reward2_val}")
    print(f"Supply at block {current_height}: {supply_info}")

def test_configuration_values():
    print("\nTesting configuration values:")
    print(f"RPC endpoint: {config.endpoint}")
    print(f"Spend confirmations: {config.spend_confirmations}")
    print(f"Block confirmations: {config.block_confirmations}")
    print(f"Block time: {config.block_time}")
    print(f"RID: {config.rid}")

if __name__ == "__main__":
    test_configuration_values()
    test_rpc_connection()
    test_reward_functions()