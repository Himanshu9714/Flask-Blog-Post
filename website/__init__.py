from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

def create_app():
    # Create an Flask app
    app = Flask(__name__)

    # To hash or encrypt session
    app.config["SECRET_KEY"] = "hellothisismysecret"

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")
    
    return app