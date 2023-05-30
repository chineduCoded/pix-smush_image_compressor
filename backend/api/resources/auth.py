"""Authentication blueprint"""
from flask import Blueprint, jsonify, request, make_response
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    get_jwt,
    unset_jwt_cookies
)
from datetime import timedelta
from ..models.user import User
from ..models.revoke_access import RevokedToken
from .. import db

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def create_user():
    """Creates a user"""
    data = request.get_json()
    user = User(**data)
    user.hash_password()
    user.save()
    return jsonify({"id": user.id}), 201


@auth_bp.route("/login", methods=["POST"])
def login_user():
    """Login a user"""
    data = request.get_json()

    user = User.query.filter_by(email=data.get("email")).first()

    if not user or not user.check_password(data.get('password')):
        return jsonify({"error": "Invalid email or password!"}), 401

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    return jsonify({"access_token": access_token, "refresh_token": refresh_token}), 200


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout_user():
    """Log out a current user"""
    # Invalidating JWT token
    jti = get_jwt()["jti"]
    revoked_token = RevokedToken(jti=jti)
    revoked_token.save_token()

    # Clearing JWT cookie
    response = make_response(
        jsonify({"message": "User logged out successfully"}), 200)
    unset_jwt_cookies(response)

    # Return a response
    return response


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    user = get_jwt_identity()

    access_token = create_access_token(identity=user)
    return jsonify({"access_token": access_token})
