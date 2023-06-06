import os
from flask import Blueprint, jsonify, request, current_app
from werkzeug.utils import secure_filename
from PIL import Image as PILImage, ExifTags
import json
import base64
from .. import db
from ..models.image import Image, ImageBlob
from ..utils.helper_func import (
    calculate_compression_ratio,
    is_supported_format,
    is_within_threshold,
    is_exceeds_max_size,
    allowed_file,
    get_image_filesize,
    get_size_format,
    get_file_extension
)
from ..utils.compress_lossless import compress_image
from ..utils.custom_jsonencoder import MyEncoder
from ..utils.get_compress_size import get_compressed_size as get_size

image_bp = Blueprint(
    "image_bp", __name__, url_prefix="/api"
)


def extract_exif_data(image):
    exif_data = image.getexif()
    if exif_data is not None:
        exif_dict = {}
        for tag_id, value in exif_data.items():
            tag_name = ExifTags.TAGS.get(tag_id, tag_id)
            exif_dict[tag_name] = value
        return exif_dict
    return {}


@image_bp.route('/images/compress', methods=['POST'])
def upload_compress():
    """Compresses automatically on image upload"""

    # Get the uploaded image from the request
    image_file = request.files['image']

    # Get the uploaded image from the request
    if image_file.filename == '':
        return jsonify({"error": "No file selected."}), 400

    # Check if the file format is suitable for compression
    if not allowed_file(image_file.filename):
        return jsonify({"error": f"{image_file.filename} unsupported for image compression!"}), 400

    # Read the image data
    image_data = image_file.read()

    if is_exceeds_max_size(image_data):
        return jsonify({"error": "Only 5MB image file allowed!"}), 400

    # Generate a secure filename for the uploaded file
    filename = secure_filename(image_file.filename)
    file_size = get_image_filesize(image_file)

    # Read the image using Pillow
    image = PILImage.open(image_file)

    file_extension = get_file_extension(image)

    file_format = image.format
    color_mode = image.mode
    width = image.width
    height = image.height
    bit_depth = image.mode

    exif_dict = extract_exif_data(image)
    exif_json = json.dumps(exif_dict, cls=MyEncoder)

    # Check if the file size is within the compression threshold
    if not is_within_threshold(file_size):
        compressed_data = compress_image(image)
    else:
        compressed_data = image_data

    # Calculate the original and compressed file sizes

    # Calculate the original and compressed file sizes
    compressed_size = get_size(compressed_data, file_extension)
    if compressed_size is not None:
        original_size = file_size
        space_saved = original_size - compressed_size

        # Calculate the percentage and space saved
        percentage_saved = (space_saved / original_size) * 100

        compression_ratio = calculate_compression_ratio(
            original_size, compressed_size)

        # Save the compressed image to the file system
        save_path = os.path.join(current_app.config["IMAGE_UPLOAD"], filename)
        with open(save_path, "wb") as f:
            f.write(compressed_data)

        # Create a new Image object
        new_image = Image(
            file_name=filename,
            file_size=file_size,
            compressed_size=compressed_size,
            percentage_saved=percentage_saved,
            space_saved=space_saved,
            compression_ratio=compression_ratio,
            file_format=file_format,
            color_mode=color_mode,
            width=width,
            height=height,
            bit_depth=bit_depth,
            exif_data=exif_json
        )

        # Store the new image in the database
        db.session.add(new_image)
        db.session.commit()

        # Create a new ImageBlob object for storing the compressed image data
        new_image_blob = ImageBlob(
            image_id=new_image.id,
            filepath=save_path,
            compressed_data=compressed_data
        )

        # Store the compressed image blob in the database
        db.session.add(new_image_blob)
        db.session.commit()

        # Return the saved image data and compression statistics
        response_data = {
            "message": "successful!",
            "compressed_size": get_size_format(new_image.compressed_size),
            "original_size": get_size_format(new_image.file_size),
            "filename": new_image.file_name,
            "width": new_image.width,
            "height": new_image.height,
            "space_saved": get_size_format(new_image.space_saved),
            "compression_ratio": new_image.compression_ratio,
            "percentage_saved": new_image.percentage_saved,
        }

        # Return a success response
        return jsonify(response_data), 200
    else:
        # Handle error appropriately
        return jsonify({"error": "Failed to obtain compressed size."}), 500
