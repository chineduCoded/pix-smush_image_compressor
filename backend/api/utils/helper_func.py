"""Helper Functions"""
from PIL import Image
import io


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024


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


def allowed_file(filename):
    """Check for the allowed file"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def is_exceeds_max_size(image_data):
    """Check if the file size exceeds the maximum limit"""
    return len(image_data) > MAX_FILE_SIZE


def is_supported_format(file_format):
    """Check if the file format is suitable for compression"""
    supported_format = ['jpg', 'jpeg', 'png', 'webp']
    return file_format in supported_format


def is_within_threshold(file_size, threshold=100000):
    """Check if the file size is within the compression threshold"""
    return file_size <= threshold


def get_image_filesize(image_file):
    """Gets file size of an image"""

    # Open the image using Pillow
    with Image.open(image_file) as image:
        # Create a buffer to hold the image data
        buffer = io.BytesIO()

        # Save the image data to the buffer
        image.save(buffer, format=image.format)

        # Get the size of the image data in bytes
        filesize = buffer.tell()

        # Release the buffer's memory
        buffer.close()

        # Return the file size
        return filesize
