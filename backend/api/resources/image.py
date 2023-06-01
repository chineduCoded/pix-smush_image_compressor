from flask import Blueprint, jsonify, request
import cv2
import numpy as np
from .. import db
from ..models.user import User
from ..models.image import Image
from ..utils.helper_func import calculate_compression_ratio
from ..utils.lossless_func import compress_lossless

image_bp = Blueprint(
    "image_bp",
    __name__,
    url_prefix="/api"
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

    # Read the image using OpenCV
    image = cv2.imdecode(np.fromstring(
        image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    # Convert the image to a different color space (e.g., BGR to HSV)
    converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract image metadata
    filename = image_file.file_name
    file_size = len(image_file.read())
    file_format = filename.split('.')[-1]
    width = image.shape[1]
    height = image.shape[0]
    color_mode = converted_image.shape[2]
    bit_depth = image.dtype.itemsize * 8
    compression_type = image.compression_type
    exif_data = {
        "camera_make": image._getexif().get(0x010f),
        "camera_model": image._getexif().get(0x0110)
    }

    # Customizable compression settings
    compression_settings = {
        'block_size': 8
    }

    # Compress the image
    compressed_data = compress_lossless(image, compression_settings)

    # Create a new Image object
    new_image = Image(file_name=filename, file_size=file_size, file_format=file_format, color_mode=color_mode, width=width,
                      height=height, bit_depth=bit_depth, compression_type=compression_type, exif_data=exif_data, compressed_data=compressed_data)

    # Store the new image in the database
    db.session.add(new_image)
    db.session.commit()

    # Return a success response
    return jsonify({'message': 'Image compressed and metadata stored in the database'})
