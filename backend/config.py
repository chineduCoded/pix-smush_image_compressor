"""Flask App Configuration"""

from os import environ, path
from dotenv import load_dotenv
from datetime import timedelta

# Specify a `.env` file containing key/value config values
basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))


class Config:
    """Set Flask config variables"""

    # General Config
    FLASK_APP = environ.get("FLASK_APP")
    SECRET_KEY = environ.get("SECRET_KEY")
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=7)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)


class DevConfig(Config):
    """Development config."""
    FLASK_ENV = "development"
    FLASK_APP = True
    SQLALCHEMY_DATABASE_URI = environ.get("DEV_DATABASE_URI")
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProdConfig(Config):
    """Production config"""
    FLASK_ENV = "production"
    FLASK_DEBUG = False
    SQLALCHEMY_DATABASE_URI = environ.get("PROD_DATABASE_URI")
