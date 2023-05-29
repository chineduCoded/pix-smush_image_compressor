"""Flask App Configuration"""

from os import environ, path
from dotenv import load_dotenv

# Specify a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

class Config:
    """Set Flask config variables"""

    # General Config
    FLASK_APP = environ.get("FLASK_APP")
    SECRET_KEY = environ.get("JWT_SECRET_KEY")
    # STATIC_FOLDER = environ.get("STATIC_FOLDER")
    # TEMPLATES_FOLDER = environ..get("TEMPLATES_FOLDER")


class DevConfig(Config):
    """Development config."""
    FLASK_ENV  = "development"
    FLASK_APP = True
    SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProdConfig(Config):
    """Production config"""
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get("PROD_DATABASE_URI")

