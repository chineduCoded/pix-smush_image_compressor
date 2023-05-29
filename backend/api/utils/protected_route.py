"""A decorator to protect routes"""
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps
from ..models.user import User


def protected(func):
    @wraps(func)
    @jwt_required
    def decorated(*args, **kwargs):
        current_user_id = get_jwt_identity()

        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "Unauthorized access"}), 403

        # Call the decorated function
        return func(*args, **kwargs)

    return decorated
