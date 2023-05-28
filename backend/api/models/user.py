"""User data models"""
from .. import db
import uuid

class User(db.Model):
    """User model"""
    __tablename__ = "users"
    id = db.Column(db.String(60), primary_key=True, default=str(uuid.uuid4()))
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)

    def __repr__(self):
        return "<User {}".format(self.username)
