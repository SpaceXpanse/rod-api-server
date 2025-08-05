import sys
import os

# Add the server directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'server'))

# Monkey patch eventlet before importing anything else
try:
    import eventlet
    eventlet.monkey_patch()
except:
    pass

def test_general_getprice():
    """Test General.getprice() method directly"""
    print("Testing General.getprice() method directly...")
    
    try:
        from server.methods.general import General
        print("Successfully imported General class")
        
        # Call the method
        result = General.getprice()
        print(f"Method returned: {result}")
        return result
    except Exception as e:
        print(f"Error calling General.getprice(): {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_general_getprice()
    if result:
        print(f"Final result: {result}")
    else:
        print("Failed to get result")