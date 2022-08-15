from flask import Blueprint, render_template

# Creating blueprint and linked to flask app
views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", name="Ram")