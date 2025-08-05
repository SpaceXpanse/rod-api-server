import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from server.methods.block import Block

def test_range():
    try:
        print("Testing range method...")
        result = Block().range(100, 3)
        print("Range method result:", result)
    except Exception as e:
        print("Error in range method:", str(e))
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_range()