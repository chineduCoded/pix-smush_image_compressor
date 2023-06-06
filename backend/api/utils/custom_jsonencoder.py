"""Custom JSON encoder"""
import json
import numpy as np
import base64
from PIL.ExifTags import TAGS
from PIL.TiffTags import TAGS as TIFF_TAGS
from PIL.TiffImagePlugin import IFDRational


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
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, IFDRational):
            return float(obj)
        if isinstance(obj, (tuple, list)):
            return list(obj)
        if isinstance(obj, dict):
            return {TAGS.get(key, key): value for key, value in obj.items()}
        if isinstance(obj, dict):
            return {TIFF_TAGS.get(key, key): value for key, value in obj.items()}
        return super().default(obj)
