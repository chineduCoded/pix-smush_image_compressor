from flask import Flask
import config
from flask_sqlalchemy import SQLAlchemy
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

        # db
        db.drop_all()
        db.create_all()

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        return app
