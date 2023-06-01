from .. import db
import uuid
from datetime import datetime
from .qrcode import QRCode


class Image(db.Model):
    """Image model"""
    __tablename__ = "images"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(60), db.ForeignKey(
        'user.id', ondelete="CASCADE"), nullable=False)
    qr_code = db.relationship(
        'QRCode', uselist=False, backref="image", cascade="all, delete-orphan")
    image_url = db.Column(db.String(200))
    download_url = db.Column(db.String(200))
    qr_code_url = db.Column(db.String(200))
    file_name = db.Column(db.String(200))
    file_size = db.Column(db.Integer)
    file_format = db.Column(db.String(10))
    width = db.Column(db.Integer)
    height = db.Column(db.Integer)
    color_mode = db.Column(db.String(40))
    bit_depth = db.Column(db.String)
    image_description = db.Column(db.String)
    compression_type = db.Column(db.String(20))
    exif_data = db.Column(db.JSON)
    compressed_url = db.Column(db.String(200))
    upload_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def generate_download_url(self):
        """
        Generates the download URL based on the image's ID.
        Assumes that the download route is mapped to '/api/download'.
        """
        base_url = 'https://127.0.0.1'  # Replace with your base URL
        download_url = f'{base_url}/api/download/{self.id}'
        self.download_url = download_url

    def generate_image_url(self):
        """
        Generates the image URL based on the image's ID.
        Assumes that the images route is mapped to /api/images
        """
        base_url = 'https://127.0.0.1'  # Replace with your base URL
        self.image_url = f'{base_url}/images/{self.id}'

    def get_compression_data(self):
        """
        Returns the compression data of the image.
        """
        compression_data = {
            'id': self.id,
            'file_name': self.file_name,
            'file_size': self.file_size,
            'file_format': self.file_format,
            'width': self.width,
            'height': self.height,
            'color_mode': self.color_mode,
            'bit_depth': self.bit_depth,
            'compression_type': self.compression_type,
        }
        return compression_data

    def __repr__(self):
        return f"Image(id={self.id}, user_id={self.user_id}, filename={self.file_name})"
