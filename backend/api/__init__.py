from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
#import connexion
#from .. import config


db = SQLAlchemy()


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    #app = connexion.App(__name__, specification_dir="../")
    #app.add_api("swagger.yml")
    app.config.from_object('config.DevConfig')

    # Initialize Plugins
    db.init_app(app)

    with app.app_context():
        # Includes routes
        from api.resources import home
        from api.resources import user

        # db
        #db.drop_all()
        db.create_all()

        # Register Blueprints
        app.register_blueprint(home.home_bp)
        app.register_blueprint(user.user_bp)

        return app
