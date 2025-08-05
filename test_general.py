import config
import requests
import json
from server.methods.general import General

def test_general_methods():
    print("Testing General methods:")
    
    # Test that configuration values are being used correctly
    print(f"Config spend_confirmations: {config.spend_confirmations}")
    print(f"Config block_confirmations: {config.block_confirmations}")
    
    # Test fee method which uses spend_confirmations
    fee_result = General.fee()
    print(f"Fee method result: {fee_result}")
    
    # Test that the result contains the correct blocks value from config
    if "result" in fee_result and "blocks" in fee_result["result"]:
        print(f"Fee method uses config.spend_confirmations: {fee_result['result']['blocks'] == config.spend_confirmations}")

if __name__ == "__main__":
    test_general_methods()