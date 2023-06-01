from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_cache import Cache
# import connexion
# from .. import config

bcrypt = Bcrypt()
db = SQLAlchemy()
jwt = JWTManager()
cache = Cache()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    # app = connexion.App(__name__, specification_dir="../")
    # app.add_api("swagger.yml")
    app.config.from_object('config.DevConfig')

    # Initialize Plugins
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    cache.init_app(app)

    with app.app_context():
        # Includes routes
        from api.resources import home
        from api.resources import user
        from api.resources import auth
        from api.resources import image

        # db
        # db.drop_all()
        db.create_all()

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(user.user_bp)
        app.register_blueprint(auth.auth_bp)
        app.register_blueprint(image.image_bp)

        return app
