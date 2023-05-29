"""User blueprint"""
from flask import Blueprint, jsonify, request
from ..models.user import User
from .. import db

user_bp = Blueprint(
        "user_bp",
        __name__,
        url_prefix="/api/v1"
)


@user_bp.route("/users", methods=["GET"])
def get_users():
    """Gets all users"""
    users = User.query.all()
    users_list = [user.to_json() for user in users]
    return jsonify(users_list)

@user_bp.route("/users/<user_id>", methods=["GET"])
def get_user(user_id):
    """Get a single user"""
    pass

@user_bp.route("/users/<user_id>", methods=["PUT"])
def update_user(user_id):
    """Updates a user"""
    body = request.get_json()
    user = User.query.get(user_id)
    if user:
        user.username = body.get("username", user.username)
        db.session.commit()
        return f"User {user_id} updated", 200
    else:
        return "Update not successfully!"

@user_bp.route("/users/<user_id>", methods=["DELETE"])
def delete_user(user_id):
    """Deletes a user"""
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return f"User {user_id} deleted successfully!", 200
    return "Deletion not successful!"
    db.session.commit()
