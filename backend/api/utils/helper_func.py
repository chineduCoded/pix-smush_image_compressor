"""Helper Functions"""
import io
import os
import shutil
import tempfile
import base64

from flask import current_app
from PIL import Image, ExifTags
import numpy as np
from sqlalchemy.orm.exc import NoResultFound

from ..models.image import ImageBlob


ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'webp'}
MAX_FILE_SIZE = 5 * 1024 * 1024


def get_file_extension(image_path):
    try:
        with Image.open(image_path) as img:
            return img.format.lower()
    except OSError:
        return None


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


def get_original_format(image_id):
    """
    Retrieves the original file format of an image based on its ID.

    Args:
        image_id (str): The ID of the image.

    Returns:
        str: The original file format of the image (e.g., 'png', 'jpeg', 'jpg', 'webp').
        None: If the file format could not be determined or the image does not exist.
    """
    try:
        image_blob = ImageBlob.query.filter_by(image_id=image_id).first()

        if image_blob is None:
            return None

        image_file_path = image_blob.file_name

        with Image.open(image_file_path) as image:
            original_format = image.format
            return original_format.lower() if original_format else None
    except NoResultFound:
        return None
    except (IOError, FileNotFoundError):
        return None


def save_image_data(image_data, filename):
    """Save the compressed image to the file system and return the file path.

    Args:
        image_data (bytes): Compressed image data.
        filename (str): Name of the file.

    Returns:
        str: File path of the saved image.
    """
    # Generate the save path by joining the configured image upload directory and the filename
    save_path = os.path.join(current_app.config["IMAGE_UPLOAD"], filename)

    # Check if the file with the same filename already exists
    if os.path.exists(save_path):
        # Append a unique suffix to the filename to avoid duplication
        file_root, file_ext = os.path.splitext(filename)
        suffix = 1
        while os.path.exists(save_path):
            new_filename = f"{file_root}_{suffix}{file_ext}"
            save_path = os.path.join(
                current_app.config["IMAGE_UPLOAD"], new_filename)
            suffix += 1

    # Create a temporary file to save the compressed image
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(image_data)
        temp_file_path = temp_file.name

    # Move the temporary file to the save path
    shutil.move(temp_file_path, save_path)

    return save_path


def decode_image_data(encoded_image_data):
    """Decodes encoded image data"""
    if encoded_image_data:
        decoded_image_data = base64.b64decode(encoded_image_data)
        image = Image.open(io.BytesIO(decoded_image_data))
        return image
    return None
