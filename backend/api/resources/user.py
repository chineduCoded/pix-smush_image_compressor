"""User blueprint"""
from flask import Blueprint, jsonify, request
from ..models.user import User
from .. import db
from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
# from ..utils.protected_route import protected

user_bp = Blueprint(
    "user_bp",
    __name__,
    url_prefix="/api"
)


@user_bp.route("/users", methods=["GET"])
@jwt_required()
def get_users():
    """Gets all users"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.is_admin:
        return jsonify({"error": "Permission denied!"})

    users = User.query.all()
    users_list = [user.to_json() for user in users]
    return jsonify(users_list), 200


@user_bp.route("/users/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    """Get a single user"""
    # Request validation
    if not user_id:
        return jsonify({"error": "User ID required!"}), 400

    # User existence
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_json()), 200


@user_bp.route("/users/<user_id>", methods=["PUT"])
@jwt_required()
def update_user(user_id):
    """Updates a user"""
    body = request.get_json()

    # Request validation
    if not user_id:
        return jsonify({"error": "User ID required!"}), 400

    # User existence
    user = User.query.get(user_id)
    if user:
        user.username = body.get("username", user.username)
        user.is_admin = body.get("is_admin", user.is_admin)
        db.session.commit()

        return jsonify({"error": f"User {user_id} updated"}), 200
    else:
        return jsonify({"error": "User not found!"}), 404


@user_bp.route("/users/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user(user_id):
    """Deletes a user"""
    # Request validation
    if not user_id:
        return jsonify({"error": "User ID required"}), 400

    # user existence
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user_id} deleted successfully!"}), 200

    return jsonify({"error": "User not found!"}), 404
    db.session.commit()


@user_bp.route("/users/logged-in", methods=["GET"])
@jwt_required()
def get_logged_in_users():
    """Get all logged-in users"""
    current_user_id = get_jwt_identity()
    current_user = User.query.get(current_user_id)

    if not current_user.is_admin:
        return jsonify({"error": "Permission denied!"})

    logged_in_users = User.query.filter(User.id != current_user_id).all()
    logged_in_users_list = [user.to_json() for user in logged_in_users]
    return jsonify(logged_in_users_list)
