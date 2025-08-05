def analyze_supply():
    """
    Analyze the SpaceXpanse ROD supply calculation
    
    Block reward: 800 ROD per block
    Halving interval: 1,054,080 blocks (approximately annually)
    Genesis premine: 199,999,998 ROD
    Total halvings: 64
    """
    
    # Parameters
    premine = 199999998.0
    block_reward = 800.0
    halving_interval = 1054080
    max_halvings = 64
    
    print("SpaceXpanse ROD Supply Analysis")
    print("=" * 50)
    print(f"Genesis premine: {premine:,} ROD")
    print(f"Block reward: {block_reward} ROD per block")
    print(f"Halving interval: {halving_interval:,} blocks")
    print(f"Total halvings: {max_halvings}")
    print()
    
    # Calculate supply from block rewards (geometric series)
    print("Block Reward Schedule:")
    print("-" * 30)
    
    total_block_supply = 0.0
    for i in range(max_halvings):
        period_reward = halving_interval * block_reward
        total_block_supply += period_reward
        print(f"Halving {i+1}: {block_reward:,.8f} ROD/block × {halving_interval:,} blocks = {period_reward:,.2f} ROD")
        
        if i < 10 or i >= max_halvings - 3:  # Show first 10 and last 3
            pass
        elif i == 10:
            print("...")
            
        block_reward /= 2.0
    
    print()
    print("Supply Calculation:")
    print("-" * 30)
    print(f"Genesis premine: {premine:,.2f} ROD")
    print(f"Block rewards: {total_block_supply:,.2f} ROD")
    max_supply = premine + total_block_supply
    print(f"Maximum supply: {max_supply:,.2f} ROD")
    print()
    
    # Convert to satoshis (8 decimal places)
    max_supply_satoshis = int(max_supply * 100000000)
    print(f"Maximum supply in satoshis: {max_supply_satoshis:,}")
    print()
    
    # Compare with Coinpaprika data
    print("Comparison with Coinpaprika Data:")
    print("-" * 30)
    coinpaprika_total_supply = 1569062124
    coinpaprika_max_supply = 4615066365
    
    print(f"Coinpaprika total supply: {coinpaprika_total_supply:,} ROD")
    print(f"Coinpaprika max supply: {coinpaprika_max_supply:,} ROD")
    print(f"Our calculated max supply: {max_supply:,.0f} ROD")
    print(f"Difference: {abs(coinpaprika_max_supply - max_supply):,.0f} ROD")
    print()
    
    # Check if there's 3% inflation after 5 years
    print("Checking for 3% inflation after 5 years:")
    print("-" * 40)
    
    # After 5 years of halving (5 halvings)
    blocks_after_5_years = 5 * halving_interval
    print(f"Blocks after 5 years: {blocks_after_5_years:,}")
    
    # Calculate supply after 5 years
    supply_after_5_years = premine
    reward = 800.0
    remaining_blocks = blocks_after_5_years
    
    for i in range(5):
        if remaining_blocks >= halving_interval:
            supply_after_5_years += halving_interval * reward
            remaining_blocks -= halving_interval
        else:
            supply_after_5_years += remaining_blocks * reward
            remaining_blocks = 0
        reward /= 2.0
    
    print(f"Supply after 5 years of halving: {supply_after_5_years:,.2f} ROD")
    
    # If there's 3% inflation for another 59 years
    # This would be additional supply beyond the halving model
    years_remaining = 59
    inflation_rate = 0.03
    
    # Calculate 3% inflation on the supply after 5 years
    additional_supply = 0.0
    current_supply = supply_after_5_years
    
    print(f"\n3% annual inflation for {years_remaining} years:")
    for year in range(1, years_remaining + 1):
        annual_inflation = current_supply * inflation_rate
        additional_supply += annual_inflation
        current_supply += annual_inflation
        if year <= 5 or year > years_remaining - 3:
            print(f"Year {year}: +{annual_inflation:,.2f} ROD (total: {current_supply:,.2f} ROD)")
        elif year == 6:
            print("...")
    
    print(f"\nTotal supply with 3% inflation: {current_supply:,.2f} ROD")
    print(f"Additional supply from inflation: {additional_supply:,.2f} ROD")
    
    # Compare with Coinpaprika max supply
    print(f"\nCoinpaprika max supply: {coinpaprika_max_supply:,} ROD")
    print(f"Difference: {abs(coinpaprika_max_supply - current_supply):,.0f} ROD")

if __name__ == "__main__":
    analyze_supply()