"""Custom JSON encoder"""
import json
import numpy as np


class MyEncoder(json.JSONEncoder):
    """Represent custom JSONEncoder"""

    def default(self, obj):
        if isinstance(obj, np.int16):
            return int(obj)  # Convert NumPy integer types to Python int
        if isinstance(obj, bytes):
            # Convert bytes to string using UTF-8 decoding
            try:
                return obj.decode("utf-8")
            except TypeError:
                return obj.decode('utf-8', 'ignore')
        if isinstance(obj, tuple):
            return list(obj)  # Convert tuples to lists
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super().default(obj)
