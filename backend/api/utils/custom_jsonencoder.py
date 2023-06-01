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
            return obj.decode("utf-8")
        if isinstance(obj, tuple):
            return list(obj)  # Convert tuples to lists

        return super().default(obj)
