"""Helper Functions"""
import os
from PIL import Image, ExifTags
import io
import numpy as np
import cv2
import heapq


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024


def get_file_extension(filename):
    supported_extensions = ['.jpg', '.jpeg', '.png', '.webp']
    file_extension = os.path.splitext(filename)[1]
    if file_extension.lower() in supported_extensions:
        return file_extension.lower()
    else:
        raise ValueError("Unsupported file extension")


def calculate_compression_ratio(original_size, compressed_size):
    """Calculate compression ratio"""
    if compressed_size == 0:
        return 0
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
    if file_size is None:
        return False
    return file_size <= threshold


def get_image_filesize(image_file):
    try:
        image_file.seek(0, os.SEEK_END)  # Move to the end of the file
        filesize = image_file.tell()  # Get the file size
        image_file.seek(0)  # Move back to the beginning of the file
        return filesize
    except (IOError, SyntaxError) as e:
        print(f"Error: {e}")
        return 0


def extract_exif_data(image):
    """
    Extracts the Exif data from the provided Pillow Image object.

    Args:
        image (PIL.Image.Image): The image object.

    Returns:
        dict: A dictionary containing the extracted Exif data.
    """
    exif_data = image.getexif()
    if exif_data is not None:
        exif_dict = {}
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            exif_dict[tag_name] = value
        return exif_dict
    return {}


def get_size_format(b, factor=1024, suffix="B"):
    """
    Scale bytes to its proper byte format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if b < factor:
            return f"{b:.2f}{unit}{suffix}"
        b /= factor
    return f"{b:.2f}Y{suffix}"
