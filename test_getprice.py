import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from server import utils
from server.methods.general import General

def test_getprice():
    print("Testing utils.getprice() directly:")
    try:
        result = utils.getprice()
        print(f"utils.getprice() result: {result}")
    except Exception as e:
        print(f"Error in utils.getprice(): {e}")
        import traceback
        traceback.print_exc()
    
    print("\nTesting General.getprice() method:")
    try:
        result = General.getprice()
        print(f"General.getprice() result: {result}")
    except Exception as e:
        print(f"Error in General.getprice(): {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_getprice()