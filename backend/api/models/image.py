from flask import current_app
from .. import db
import uuid
from datetime import datetime
from .qrcode import QRCode
from urllib.parse import quote_plus


class Image(db.Model):
    """Image model"""
    __tablename__ = "images"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    """user_id = db.Column(db.String(60), db.ForeignKey(
        'users.id', ondelete="CASCADE"), nullable=False)"""
    """qr_code = db.relationship(
        'QRCode', uselist=False, backref="image", cascade="all, delete-orphan")"""
    image_url = db.Column(db.String(200))
    download_url = db.Column(db.String(200))
    qr_code_url = db.Column(db.String(200))
    file_name = db.Column(db.String(200))
    file_size = db.Column(db.Integer)
    file_format = db.Column(db.String(10))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    color_mode = db.Column(db.String(40))
    bit_depth = db.Column(db.SmallInteger)
    image_description = db.Column(db.String(100))
    compression_type = db.Column(db.String(20))
    exif_data = db.Column(db.JSON)
    compressed_url = db.Column(db.String(200))
    compressed_data = db.Column(db.JSON)
    upload_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def generate_download_url(self):
        """
        Generates the download URL based on the image's file name.
        Assumes that the download route is mapped to '/api/downloads'.
        """
        base_url = current_app.config["BASE_URL"]  # Replace with your base URL
        encoded_name = quote_plus(self.file_name)
        download_url = base_url + encoded_name
        self.download_url = download_url
        return download_url

    def generate_image_url(self):
        """
        Generates the image URL based on the image's file name.
        Assumes that the images route is mapped to /api/images
        """
        base_url = current_app.config["BASE_URL"]  # Replace with your base URL
        encoded_name = quote_plus(self.file_name)
        image_url = base_url + encoded_name
        self.image_url = image_url
        return image_url

    def get_compression_data(self):
        """
        Returns the compression data of the image.
        """
        compression_details = {
            'id': self.id,
            'file_name': self.file_name,
            'original_size': self.file_size,
            'file_format': self.file_format,
            'width': self.width,
            'height': self.height,
            'color_mode': self.color_mode,
            'bit_depth': self.bit_depth,
            'compression_type': self.compression_type,
            'exif_data': self.exif_data,
            'image_url': self.generate_image_url(),
            'download_url': self.generate_download_url(),
            'uploaded_at': self.upload_at
        }
        return compression_details

    def __repr__(self):
        return f"Image(id={self.id}, user_id={self.user_id}, filename={self.file_name})"
