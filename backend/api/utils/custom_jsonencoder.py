"""Custom JSON encoder"""
import json
import numpy as np
import base64


class MyEncoder(json.JSONEncoder):
    """Represent custom JSONEncoder"""

    def default(self, obj):
        if isinstance(obj, np.int16):
            return int(obj)  # Convert NumPy integer types to Python int
        if isinstance(obj, bytes):
            # Convert bytes to string using UTF-8 decoding
            try:
                return {
                    '__type__': 'bytes',
                    'value': base64.b64encode(obj).decode('utf-8')
                }
            except TypeError:
                return obj.decode('utf-8', 'ignore')
        if isinstance(obj, tuple):
            return list(obj)  # Convert tuples to lists
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
