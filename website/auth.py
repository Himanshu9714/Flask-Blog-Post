from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User

# Creating blueprint and linked to flask app
auth = Blueprint("auth", __name__)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Get the user data from form
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            # Check if password matches
            if check_password_hash(user.password, password):
                flash("Logged In!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect!", category="error")
        else:
            flash("Email doesn't exist!", category="error")

    return render_template("login.html")


@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        # Get the user data from form
        username = request.form.get("username")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        # Check if user already exists
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        if email_exists:
            flash("Email is already in use.", category="error")
        elif username_exists:
            flash("Username is already in use.", category="error")
        elif password1 != password2:
            flash("Password don't match!", category="error")
        elif len(username) < 2:
            flash("Username is too short!", category="error")
        elif len(password1) < 6:
            flash("Password is too short!", category="error")
        # TODO: Validates email address properly
        elif len(email) < 10 or "@" not in email:
            flash("Email is invalid!", category="error")
        else:
            # Create user account if validation completes
            new_user = User(
                email=email,
                username=username,
                password=generate_password_hash(password1, method="sha256"),
            )
            # Staging area
            db.session.add(new_user)
            # Writing to db
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User Created!")
            return redirect(url_for("views.home"))

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))
