"""Store Revoke Access Token"""
from .. import db
import uuid
from datetime import datetime


class RevokedToken(db.Model):
    """Represent Revoked Token"""
    __tablename__ = "revoked"
    id = db.Column(db.String(60), primary_key=True, unique=True,
                   default=lambda: str(uuid.uuid4()))
    jti = db.Column(db.String(128), unique=True, nullable=False)
    revoked_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)

    def __init__(self, jti):
        self.jti = jti

    def save_token(self):
        db.session.add(self)
        db.session.commit()
