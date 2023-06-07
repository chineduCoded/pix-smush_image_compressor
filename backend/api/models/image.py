from flask import current_app
from .. import db
import uuid
from datetime import datetime
from .qrcode import QRCode
import json


class Image(db.Model):
    """Image model"""
    __tablename__ = "images"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    """qr_code = db.relationship(
        'QRCode', uselist=False, backref="image", cascade="all, delete-orphan")"""
    """image_url = db.Column(db.String(200))
    download_url = db.Column(db.String(200))
    qr_code_url = db.Column(db.String(200))"""
    blob = db.relationship(
        "ImageBlob", uselist=False, backref="images", cascade='all, delete-orphan')
    file_name = db.Column(db.String(255))
    file_size = db.Column(db.Integer)
    compressed_size = db.Column(db.Integer)
    percentage_saved = db.Column(db.Numeric(precision=7, scale=2))
    space_saved = db.Column(db.Integer)
    compression_ratio = db.Column(db.Numeric(precision=7, scale=1))
    file_format = db.Column(db.String(10))
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

    def __repr__(self):
        return f"Image(id={self.id}, filename={self.file_name})"


class ImageBlob(db.Model):
    """Holds image Blob"""
    __tablename__ = "blobs"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    image_id = db.Column(db.String(60), db.ForeignKey(
        "images.id", ondelete="CASCADE"), primary_key=True)
    file_name = db.Column(db.String(255))
    filepath = db.Column(db.String(255))
    compressed_data = db.Column(db.LargeBinary(length=(2**32) - 1))

    def __repr__(self):
        return f"ImageBlob(image_id={self.image_id})"
