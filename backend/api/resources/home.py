"""Home Blueprint"""
from flask import Blueprint, jsonify

# Blueprint Configuration
home_bp = Blueprint(
        'home_bp', __name__,
        template_folder='templates',
        static_folder='static'
)


@home_bp.route('/', methods=['GET'])
def home():
    """Home Screen"""
    return jsonify({"message": "PixSmush API"}), 200



