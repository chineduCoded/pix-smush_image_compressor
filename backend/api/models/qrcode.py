from .. import db
import uuid
from datetime import datetime
import qrcode
import io


class QRCode(db.Model):
    """QR code model"""
    __tablename__ = 'qrcode'
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    image_id = db.Column(db.String(60), db.ForeignKey(
        'images.id', ondelete="CASCADE"), nullable=False)
    qr_code_image_url = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    description = db.Column(db.String(60))
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    @property
    def qr_code_data(self):
        return self.generate_qrcode()

    def generate_qrcode(self):
        """Generate the PNG QR code"""
        qr = qrcode.QRCode(version=1, box_size=10, border=4)

        # Access the associated image through the relationship
        image = self.image

        # You can modify the data to be encoded in the QR code
        qr.add_data(image.file_name)
        qr.make(fit=True)
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # Save the QR code image to a BytesIO buffer
        qr_code_buffer = io.BytesIO()
        qr_image.save(qr_code_buffer, format='PNG')

        # Return the QR code data as binary
        return qr_code_buffer.getvalue()
