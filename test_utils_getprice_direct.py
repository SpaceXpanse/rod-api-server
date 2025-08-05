import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from server.utils import getprice

print("Testing utils.getprice() directly:")
result = getprice()
print(f"Result: {result}")