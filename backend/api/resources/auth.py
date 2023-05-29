"""Authentication blueprint"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import create_access_token
from datetime import timedelta
from ..models.user import User
from .. import db

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/v1")


@auth_bp.route("/register", methods=["POST"])
def create_user():
    """Creates a user"""
    body = request.get_json()
    user = User(**body)
    user.hash_password()
    user.save()
    return jsonify({"id": user.id}), 201

@auth_bp.route("/login", methods=["POST"])
def login_user():
    """Login a user"""
    body = request.get_json()
    user = User.query.filter_by(email=body.get("email")).first()

    if not user or not user.check_password(body.get('password')):
        return jsonify({"error": "Invalid email or password!"}), 401
    
    expires = timedelta(days=7)
    access_token = create_access_token(identity=user.id, expires_delta=expires)
    return jsonify({"token": access_token}), 200