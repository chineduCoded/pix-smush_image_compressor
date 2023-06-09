import os
from flask import Blueprint, jsonify, request, current_app, send_file
from werkzeug.utils import secure_filename
from PIL import Image as PILImage, ExifTags
import json
from io import BytesIO
import qrcode
import mimetypes
from .. import db
from ..models.image import Image, ImageBlob
from ..utils.helper_func import (
    calculate_compression_ratio,
    is_within_threshold,
    is_exceeds_max_size,
    allowed_file,
    get_image_filesize,
    get_size_format,
    save_image_data,
    decode_image_data
)
from ..utils.compress import compress_image, decompressed_file
from ..utils.custom_jsonencoder import MyEncoder
from ..utils.get_compress_size import get_compressed_size


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

    # Get file extension
    file_ext = os.path.splitext(image_file.filename)[1].lower()

    # Calculate the original and compressed file sizes
    compressed_size = get_compressed_size(compressed_data, file_ext)
    if compressed_size is not None:
        original_size = file_size
        space_saved = original_size - compressed_size

        # Calculate the percentage and space saved
        percentage_saved = (space_saved / original_size) * 100

        compression_ratio = calculate_compression_ratio(
            original_size, compressed_size)

        # Save the compressed image to the file system
        file_path = save_image_data(compressed_data, filename)
        base_path = current_app.config["BASE_URL"]
        image_full_path = f"{base_path}/{file_path}"

        # Create a new Image object
        new_image = Image(
            file_name=filename,
            file_size=file_size,
            compressed_size=compressed_size,
            percentage_saved=percentage_saved,
            space_saved=space_saved,
            compression_ratio=compression_ratio,
            file_format=file_format,
            file_path=image_full_path,
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
            file_name=filename,
            compressed_data=compressed_data
        )

        # Store the compressed image blob in the database
        db.session.add(new_image_blob)
        db.session.commit()

        encoded_data = new_image.get_qr_code_png()
        qr_code_image = decode_image_data(encoded_data)

        # Return the saved image data and compression statistics
        response_data = {
            "message": "successful!",
            "id": new_image.id,
            "compressed_size": get_size_format(new_image.compressed_size),
            "original_size": get_size_format(new_image.file_size),
            "original_format": new_image.file_format,
            "filename": new_image.file_name,
            "image_url": new_image.file_path,
            "width": new_image.width,
            "height": new_image.height,
            "space_saved": get_size_format(new_image.space_saved),
            "compression_ratio": new_image.compression_ratio,
            "percentage_saved": new_image.percentage_saved,
            "qr_code_image": encoded_data
        }

        # Return a success response
        return jsonify(response_data), 201
    else:
        # Handle error appropriately
        return jsonify({"error": "Failed to obtain compressed size."}), 500


@image_bp.route("/download/<image_id>", methods=["GET"])
def download_image(image_id):
    """Download image file"""
    # Retrieve the image record from the database
    image = Image.query.get(image_id)

    if image is None:
        return jsonify({"error": "Image not found!"}), 404

    # Check if compressed data is available in the database
    compressed_data = image.blob.compressed_data
    try:
        if compressed_data:
            decompressed_data = decompressed_file(
                compressed_data, image.file_format)
            if decompressed_data is None:
                return jsonify({"error": "Error decompressing the image!"}), 500
        else:
            # Determine the path to the image file on the filesystem
            image_path = save_image_data(compressed_data, image.file_name)

            # Check if the image file exists
            if not os.path.exists(image_path):
                return jsonify({"error": "Image file not found!"}), 404

            # Read the image file from the filesystem
            with open(image_path, 'rb') as file:
                decompressed_data = file.read()

        # Determine the MIME type of the image based on the file extension
        mime_type, _ = mimetypes.guess_type(image.file_name)

        return send_file(
            decompressed_data[0],
            mimetype=mime_type,
            as_attachment=True,
            download_name=image.file_name
        )
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    
@image_bp.route("/qrcode/<image_id>", methods=["GET"])
def generate_qrcode(image_id):
    """
    Generates a QR code image

    Args:
        image_id (str): Image ID in string format

    Returns:
        QR code image (PNG format)
    """
    image = Image.query.get(image_id)

    if image is None:
        return jsonify({"error": "Image not found!"}), 404

    if image.file_path:

        image_path = current_app.config["BASE_URL"]
        image_url_path = f"{image_path}/{image.file_path}"


        # Generate QR code
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=5,
        )
        qr.add_data(image_url_path)  # Use image.file_path instead of image.url
        qr.make(fit=True)
        qr_img = qr.make_image()

        # Save the QR code image to a byte stream
        img_byte_stream = BytesIO()
        qr_img.save(img_byte_stream, format='PNG')
        img_byte_stream.seek(0)

        # Return the QR code image
        return send_file(img_byte_stream, mimetype='image/png')
    else:
        return jsonify({"error": "Could not generate QR code!"}), 400


@image_bp.route("/images", methods=["GET"])
def get_all_images():
    """Gets all images"""
    images = Image.query.all()
    image_list = [
        {
            "message": "successful!",
            "id": image.id,
            "compressed_size": get_size_format(image.compressed_size),
            "original_size": get_size_format(image.file_size),
            "original_format": image.file_format,
            "filename": image.file_name,
            "file_path": image.file_path,
            "width": image.width,
            "height": image.height,
            "space_saved": get_size_format(image.space_saved),
            "compression_ratio": image.compression_ratio,
            "percentage_saved": image.percentage_saved
        } for image in images]

    return jsonify(image_list), 200


@image_bp.route("/images", methods=["DELETE"])
def delete_all_images():
    # Retrieve all image records from the database
    images = Image.query.all()

    # Loop through each image and delete the corresponding file
    for image in images:
        image_path = os.path.join(
            current_app.config["IMAGE_UPLOAD"], image.file_name)
        if os.path.exists(image_path):
            os.remove(image_path)

    # Delete all image records from the database
    deleted = Image.query.delete()

    # Commit the changes to the database
    db.session.commit()

    if deleted:
        return jsonify({"message": "All images deleted successfully!"}), 200
    else:
        return jsonify({"message": "All images deleted already!"}), 404
