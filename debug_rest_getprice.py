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

def test_rest_getprice():
    """Test the REST getprice function directly"""
    print("Testing REST getprice function directly...")
    
    try:
        from server.methods.general import General
        from server import utils
        
        # Call the method exactly as the REST endpoint does
        print("Calling General().getprice()...")
        data = General().getprice()
        print(f"Method returned data: {data}")
        
        # Wrap it in utils.response as the REST endpoint does
        result = utils.response(data)
        print(f"Wrapped result: {result}")
        
        # Convert to JSON as the REST endpoint does
        from flask import jsonify
        json_result = jsonify(result)
        print(f"JSON result: {json_result}")
        
        return result
    except Exception as e:
        print(f"Error in REST getprice test: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    result = test_rest_getprice()
    if result:
        print(f"Final result: {result}")
    else:
        print("Failed to get result")