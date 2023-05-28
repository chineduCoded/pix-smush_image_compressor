from flask import Flask
#from .. import config


def create_app():
    """Initialize the core application."""
    app = Flask(__name__)
    #app.config.from_object('config.DevConfig')

    # Initialize Plugins

    with app.app_context():
        # Includes routes
        from api.resources import home

        # Register Blueprints
        app.register_blueprint(home.home_bp)

        return app
