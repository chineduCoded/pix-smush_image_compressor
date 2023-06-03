"""Image Blueprint"""
import os
from flask import Blueprint, jsonify, request
import cv2
import numpy as np
import json
from PIL import Image as PILImage
from werkzeug.utils import secure_filename
from .. import db
from ..models.user import User
from ..models.image import Image
from ..utils.helper_func import (
    calculate_compression_ratio,
    is_supported_format,
    is_within_threshold,
    is_exceeds_max_size,
    allowed_file,
    get_image_filesize
)
from ..utils.compress_lossless import compress_image
from ..utils.custom_jsonencoder import MyEncoder
import base64

image_bp = Blueprint(
    "image_bp", __name__, url_prefix="/api"
)


@image_bp.route("/images", methods=["GET"])
def get_images_with_qrcodes():
    images = Image.query.all()
    result = [{
        'image_id': image.id,
        'user_id': image.user_id,
        'filename': image.file_name,
        'image_url': image.image_url,
        'download_url': image.download_url,
        'compression_ratio': calculate_compression_ratio(image),
        'qr_code_data': image.qr_code.qr_code_data if image.qr_code else None
    } for image in images]
    return jsonify(result), 200


@image_bp.route("/images/user/<user_id>", methods=["GET"])
def get_user_images_with_qrcodes(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message': 'User not found'}), 404
    images = user.images
    result = [{
        'image_id': image.id,
        'image_url': image.image_url,
        'filename': image.file_name,
        'download_url': image.download_url,
        'qr_code_data': image.qr_code.qr_code_data if image.qr_code else None
    } for image in images]
    return jsonify(result), 200


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
    pil_image = PILImage.open(image_file)

    # Convert the image to OpenCV format (BGR)
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Convert the image to a different color space (e.g., BGR to HSV)
    converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract image metadata
    file_format = filename.split('.')[-1]
    width = image.shape[1]
    height = image.shape[0]
    color_mode = converted_image.shape[2]
    bit_depth = image.dtype.itemsize * 8

    # Extract EXIF data
    exif_data = {}
    try:
        exif_get = pil_image._getexif()
        exif_data = {
            "camera_make": exif_get.get(0x010f),
            "camera_model": exif_get.get(0x0110)
        }
    except:
        pass
    exif_data_serializable = json.dumps(exif_data, cls=MyEncoder)

    # Check if the file format is suitable for compression
    if not is_supported_format(file_format):
        return jsonify({"error": "Only JPG, JPEG, PNG, and WEBP formats are allowed!"}), 400

    # Check if the file size is within the compression threshold
    if not is_within_threshold(file_size):
        compressed_data = compress_image(image_data)
    else:
        compressed_data = image_data

    # Convert the compressed data to bytes
    compressed = compressed_data

    # Serialize the compressed data to JSON
    compressed_data_serializable = json.dumps(compressed, cls=MyEncoder)

    # Create a new Image object
    new_image = Image(
        file_name=filename,
        file_size=file_size,
        file_format=file_format,
        color_mode=color_mode,
        width=width,
        height=height,
        bit_depth=bit_depth,
        compression_type="lossless" if compressed_data != image_data else "none",
        exif_data=exif_data_serializable,
        compressed_data=compressed_data_serializable
    )

    # Store the new image in the database
    db.session.add(new_image)
    db.session.commit()

    compressed_size = len(compressed_data_serializable)
    space_saved = file_size - compressed_size
    percentage_saved = 0

    if file_size != 0:
        percentage_saved = (space_saved / file_size) * 100
        percentage_saved = round(percentage_saved, 2)

    # Return the saved image data and compression statistics
    response_data = {
        "message": "Image compressed and saved!",
        "compressed_size": compressed_size,
        "space_saved": space_saved,
        "percentage_saved": percentage_saved,
        "image_data": new_image.get_compression_data()
    }

    # Return a success response
    return jsonify(response_data), 200
