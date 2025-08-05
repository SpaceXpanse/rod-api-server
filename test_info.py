import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from server.methods.general import General

def test_info():
    try:
        print("Testing info method...")
        result = General().info()
        print("Info method result:", result)
    except Exception as e:
        print("Error in info method:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_info()