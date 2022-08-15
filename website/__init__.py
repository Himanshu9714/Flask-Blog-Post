from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

def create_app():
    # Create an Flask app
    app = Flask(__name__)

    # To hash or encrypt session
    app.config["SECRET_KEY"] = "hellothisismysecret"

    return app