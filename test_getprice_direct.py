import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

from server.utils import getprice

print("Testing getprice function directly:")
result = getprice()
print(f"Result: {result}")