import os
import uuid
from datetime import datetime
import json
import qrcode
import requests
import io
import base64

from flask import current_app
from PIL import ImageDraw, ImageFont

from .. import db


class Image(db.Model):
    """Image model"""
    __tablename__ = "images"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    blob = db.relationship(
        "ImageBlob", uselist=False, backref="images", cascade='all, delete-orphan')
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    compressed_size = db.Column(db.Integer)
    percentage_saved = db.Column(db.Numeric(precision=7, scale=2))
    space_saved = db.Column(db.Integer)
    compression_ratio = db.Column(db.Numeric(precision=7, scale=1))
    file_format = db.Column(db.String(10))
    file_path = db.Column(db.String(255))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    color_mode = db.Column(db.String(10))
    bit_depth = db.Column(db.String(10))
    exif_data = db.Column(db.JSON)
    upload_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def set_exif_data(self, exif_data):
        # Convert dictionary to JSON string
        self.exif_data = json.dumps(exif_data)

    def get_exif_data(self):
        # Parse JSON string to dictionary
        return json.loads(self.exif_data)

    def get_qr_code_png(self):
        if self.blob and self.blob.qrcode:
            qr_code_path = self.blob.qrcode.qr_code_url
            if qr_code_path:
                image_data = open(qr_code_path, "rb").read()
                encoded_image_data = base64.b64encode(
                    image_data).decode("utf-8")
                return encoded_image_data
        return None

    def __repr__(self):
        return f"Image(id={self.id}, filename={self.file_name})"


class ImageBlob(db.Model):
    """Holds image Blob"""
    __tablename__ = "blobs"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    image_id = db.Column(db.String(60), db.ForeignKey(
        "images.id", ondelete="CASCADE"), nullable=False)
    qrcode = db.relationship("QRCode", backref="qr_codes",
                             uselist=False, cascade='all, delete-orphan')
    file_name = db.Column(db.String(255))
    compressed_data = db.Column(db.LargeBinary(length=(2**32) - 1))

    def __repr__(self):
        return f"ImageBlob(image_id={self.image_id})"


class QRCode(db.Model):
    """QRCode model"""
    __tablename__ = "qrcodes"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    image_blob_id = db.Column(db.String(60), db.ForeignKey(
        "blobs.id", ondelete="CASCADE"), nullable=False)
    qr_code_data = db.Column(db.LargeBinary(length=(2**32) - 1))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Additional columns
    qr_code_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)

    def generate_qr_code(self):
        # Get the associated ImageBlob
        image_blob = ImageBlob.query.get(self.image_blob_id)

        # Generate QR code from compressed_data
        qr = qrcode.QRCode(
            version=None,
            error_correction=qrcode.constants.ERROR_CORRECT_M,
            box_size=10,
            border=4,
        )

        qr.add_data(image_blob.compressed_data)
        qr.make(fit=True)

        # Create a PNG image from the QR code
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Create a drawing object
        draw = ImageDraw.Draw(qr_image)

        # Define the text to be added
        text = "PS"

        font_url = href = "https://fonts.googleapis.com/css2?family=Leckerli+One&family=Poppins:wght@200;300;400;500;600;700;800;900&family=Rubik+Puddles&display=swap"
        response = requests.get(font_url)
        font_file_path = "font.ttf"  # Path to save the font file
        with open(font_file_path, "wb") as font_file:
            font_file.write(response.content)

        # Choose a font and its size
        font = ImageFont.truetype(font_file_path, size=24)

        # Calculate the position to place the text
        text_width, text_height = draw.textsize(text, font=font)
        text_position = ((qr_image.width - text_width) // 2,
                         qr_image.height - text_height - 10)

        # Set the text color
        text_color = (0, 0, 0)  # Black color

        # Add the text to the image
        draw.text(text_position, text, fill=text_color, font=font)

        # Save the QR code image
        qr_code_path = os.path.join(
            current_app.config['QR_CODE_SAVE_PATH'], f"qr_code_{self.id}.png")
        qr_image.save(qr_code_path)

        # Save the QR code image to a byte buffer
        qr_code_buffer = io.BytesIO()
        qr_image.save(qr_code_buffer, format='PNG')

        # Set the QR code URL
        self.qr_code_url = qr_code_path

        # Remove the font file
        os.remove(font_file_path)

        # Return the QR code image data as a file-like object
        qr_code_buffer.seek(0)
        return qr_code_buffer

    def __repr__(self):
        return f"QRCode(id={self.id}, image_blob_id={self.image_blob_id})"
