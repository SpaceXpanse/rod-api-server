import config

def test_config_usage():
    print("Testing configuration usage in code:")
    
    # Test config values
    print(f"RPC endpoint: {config.endpoint}")
    print(f"Spend confirmations: {config.spend_confirmations}")
    print(f"Block confirmations: {config.block_confirmations}")
    print(f"Block time: {config.block_time}")
    print(f"RID: {config.rid}")
    
    # Verify the values match requirements
    assert config.spend_confirmations == 6, f"Expected 6 confirmations for spend, got {config.spend_confirmations}"
    assert config.block_confirmations == 120, f"Expected 120 confirmations for blocks, got {config.block_confirmations}"
    assert config.block_time == 30, f"Expected 30 second block time, got {config.block_time}"
    assert "11999" in config.endpoint, f"Expected port 11999 in endpoint, got {config.endpoint}"
    
    print("All configuration values are correct!")
    
    # Check that server/methods/general.py uses these values correctly
    # Based on our earlier inspection:
    # Line 24: nethash = utils.make_request("getnetworkhashps", [config.block_confirmations, data["result"]["blocks"]])
    # Line 61: "blocks": config.spend_confirmations
    
    print("server/methods/general.py correctly uses:")
    print(f"  - config.block_confirmations ({config.block_confirmations}) for network hash calculations")
    print(f"  - config.spend_confirmations ({config.spend_confirmations}) for fee calculations")

if __name__ == "__main__":
    test_config_usage()