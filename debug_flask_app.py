import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server import app
from server.methods.general import General

# Test the getprice method directly
print("Testing General.getprice() directly:")
try:
    result = General().getprice()
    print(f"Result: {result}")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()

# Test with app context
print("\nTesting with app context:")
with app.app_context():
    try:
        result = General().getprice()
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()