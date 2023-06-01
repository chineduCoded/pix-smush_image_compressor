from flask import Blueprint, jsonify, request
import cv2
import numpy as np
import json
from PIL import Image as PILImage
from io import BytesIO
from werkzeug.utils import secure_filename
from .. import db
from ..models.user import User
from ..models.image import Image
from ..utils.helper_func import calculate_compression_ratio
from ..utils.lossless_func import compress_lossless
from ..utils.custom_jsonencoder import MyEncoder

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

    # Generate a secure filename for the uploaded file
    filename = secure_filename(image_file.filename)

    # Read the image using Pillow
    pil_image = PILImage.open(image_file)

    # Convert the image to OpenCV format (BGR)
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    # Convert the image to a different color space (e.g., BGR to HSV)
    converted_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extract image metadata
    file_size = image_file.content_length
    file_format = filename.split('.')[-1]
    width = image.shape[1]
    height = image.shape[0]
    color_mode = converted_image.shape[2]
    bit_depth = image.dtype.itemsize * 8

    # Extract EXIF data
    exif_get = pil_image._getexif()
    exif_data = {
        "camera_make": exif_get.get(0x010f),
        "camera_model": exif_get.get(0x0110)
    }
    exif_data_serializable = json.dumps(exif_data, cls=MyEncoder)

    # Customizable compression settings
    compression_settings = {
        'block_size': 8
    }

    # Compress the image
    compressed_data = compress_lossless(image, compression_settings)

    # Create a new Image object
    new_image = Image(
        file_name=filename,
        file_size=file_size,
        file_format=file_format,
        color_mode=color_mode,
        width=width,
        height=height,
        bit_depth=bit_depth,
        compression_type="lossless",
        exif_data=exif_data_serializable,
        compressed_data=compressed_data
    )

    # Store the new image in the database
    db.session.add(new_image)
    db.session.commit()

    compressed_size = len(compressed_data)
    space_saved = file_size - compressed_size
    percentage_saved = (space_saved / file_size) * 100

    # Return the saved image data and compression statistics
    response_data = {
        "message": "Image compressed and saved!",
        "compressed_data": new_image.get_compression_data(),
        "original_size": file_size,
        "compressed_size": compressed_size,
        "space_saved": space_saved,
        "percentage_saved": percentage_saved,
        "image_url": new_image.generate_image_url()
    }

    # Return a success response
    return jsonify(response_data)
