import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import in the same order as the server
import eventlet
eventlet.monkey_patch()

from server import config
from server import utils
from server.methods.general import General

print("Testing utils.getprice() with server imports:")
result = utils.getprice()
print(f"Result: {result}")

print("\nTesting General.getprice() with server imports:")
result = General().getprice()
print(f"Result: {result}")