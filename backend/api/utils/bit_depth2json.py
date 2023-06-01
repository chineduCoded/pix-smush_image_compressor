"""Convert bit depth to JSON serializable"""
import json
from .custom_jsonencoder import MyEncoder


def bit_depth2json_serializable(bit_depth):
    """Convert to JSON serializable"""

    # Convert the int16 value to a JSON-serializable type
    bit_depth_serializable = int(bit_depth)

    # Create a dictionary with the serializable bit depth value
    response_data = {
        "bit_depth": bit_depth_serializable
    }

    # Convert the dictionary to JSON format
    json_data = json.dumps(response_data, cls=MyEncoder)
    return json_data
