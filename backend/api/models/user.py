"""User data models"""
from .. import db
import uuid
from datetime import datetime

class User(db.Model):
    """User model"""
    __tablename__ = "users"
    id = db.Column(db.String(60), primary_key=True, unique=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_json(self):
        """Return JSON representation of the user object"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

    def __repr__(self):
        return "<User {}".format(self.username)
