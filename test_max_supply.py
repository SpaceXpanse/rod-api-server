import math

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def calculate_max_supply():
    # SpaceXpanse ROD max supply calculation
    # 800 ROD block reward with halving every 1,054,080 blocks
    # Genesis block premine: 199,999,998 ROD coins
    
    # Add genesis block premine
    premine = 199999998.0
    max_supply = premine
    
    block_reward = 800.0
    halving_interval = 1054080
    
    # Sum all halving periods (geometric series)
    for i in range(64):
        max_supply += halving_interval * block_reward
        block_reward /= 2.0
        
    print(f"Genesis premine: {premine} ROD")
    print(f"Block rewards: {max_supply - premine} ROD")
    print(f"Total max supply: {max_supply} ROD")
    print(f"Total max supply in satoshis: {satoshis(max_supply)}")
    
    return satoshis(max_supply)

# Calculate max supply
max_supply_satoshis = calculate_max_supply()
print(f"\nMax supply in satoshis: {max_supply_satoshis}")