import config
import requests
import json
import math

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def reward(height):
    # SpaceXpanse ROD block reward: 800 ROD with halving every 1,054,080 blocks
    halvings = height // 1054080
    if halvings >= 64:
        return 0
    return int(satoshis(800.00000000) // (2 ** halvings))

def reward2(blockHeight):
    # SpaceXpanse ROD block reward: 800 ROD with halving every 1,054,080 blocks
    # 75%/25% distribution (3 neoscrypt-xaya blocks and 1 SHA256d block every 4 blocks)
    # For simplicity, we'll return the average reward per block (800 ROD)
    halvings = blockHeight // 1054080
    if halvings >= 64:
        return 0
    reward = 800.0 / (2 ** halvings)
    return format(reward, '.8f')

def supply(height):
    # SpaceXpanse ROD supply calculation
    # 800 ROD block reward with halving every 1,054,080 blocks
    # 75%/25% distribution (3 neoscrypt-xaya blocks and 1 SHA256d block every 4 blocks)
    # Max supply is theoretically infinite but will be practically limited
    
    block_reward = 800.0
    halving_interval = 1054080
    total_supply = 0.0
    remaining_height = height
    halvings = 0
    
    while remaining_height >= halving_interval and halvings < 64:
        # Add supply for this halving period
        total_supply += halving_interval * block_reward
        remaining_height -= halving_interval
        block_reward /= 2.0
        halvings += 1
    
    # Add supply for remaining blocks in current period
    total_supply += remaining_height * block_reward
    
    return {
        "halvings": halvings,
        "supply": satoshis(total_supply),
        "total/max supply": "Infinite (practically limited by halvings)"
    }

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
    reward_val = reward(current_height)
    reward2_val = reward2(current_height)
    supply_info = supply(current_height)
    
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
    rpc_result = test_rpc_connection()
    test_reward_functions()