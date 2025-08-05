import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from server.methods.general import General

def test_getprice():
    try:
        print("Testing getprice method...")
        result = General().getprice()
        print("Getprice method result:", result)
    except Exception as e:
        print("Error in getprice method:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_getprice()