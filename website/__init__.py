from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    # Create an Flask app
    app = Flask(__name__)

    # To hash or encrypt session
    app.config["SECRET_KEY"] = "hellothisismysecret"

    # Config and init database
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    # Register blueprints
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    # models
    from .models import User, Post, Comment

    # Creating database
    create_database(app)

    # Allows log in and out the users
    login_manager = LoginManager()
    # If someone is not logged in then redirect them to auth.login
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app


def create_database(app):
    # If database doesn't exists create it.
    # This is not useful in production. But you can use it locally.
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")
