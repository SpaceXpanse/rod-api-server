import math

def satoshis(value):
    return math.ceil(value * math.pow(10, 8))

def supply(height):
    # SpaceXpanse ROD supply calculation
    # 800 ROD block reward with halving every 1,054,080 blocks
    # 75%/25% distribution (3 neoscrypt-xaya blocks and 1 SHA256d block every 4 blocks)
    # Max supply is capped at 4,615,066,365 ROD coins
    # Genesis block premine: 199,999,998 ROD coins
    
    # Add genesis block premine
    premine = 199999998.0
    total_supply = premine
    
    block_reward = 800.0
    halving_interval = 1054080
    remaining_height = height
    halvings = 0
    
    print(f"Calculating supply for height: {height}")
    print(f"Genesis premine: {premine} ROD")
    
    while remaining_height >= halving_interval and halvings < 64:
        # Add supply for this halving period
        period_supply = halving_interval * block_reward
        total_supply += period_supply
        print(f"Halving {halvings}: Added {period_supply} ROD (reward: {block_reward} ROD)")
        remaining_height -= halving_interval
        block_reward /= 2.0
        halvings += 1
    
    # Add supply for remaining blocks in current period
    remaining_supply = remaining_height * block_reward
    total_supply += remaining_supply
    print(f"Remaining blocks {remaining_height}: Added {remaining_supply} ROD (reward: {block_reward} ROD)")
    
    print(f"Total supply: {total_supply} ROD")
    print(f"Total supply in satoshis: {satoshis(total_supply)}")
    
    return {
        "halvings": halvings,
        "supply": satoshis(total_supply),
        "total/max supply": "4,615,066,365 ROD coins"
    }

# Test with current height
current_height = 3103967
result = supply(current_height)
print(f"\nResult: {result}")