"""Helper Functions"""
from PIL import Image
import io


def calculate_compression_ratio(compressed_image):
    """calculate compression ratio"""
    original_size = len(compressed_image.compressed_data)
    compressed_size = original_size
    compression_ratio = original_size / compressed_size
    return compression_ratio


def get_image_dimensions(compressed_data):
    """Get image dimensions"""
    # Create a temporary in-memory file object
    image_file = io.BytesIO(compressed_data)

    # Open the image using Pillow without fully decoding it
    with Image.open(image_file) as image:
        width, height = image.size

    return {'width': width, 'height': height}
