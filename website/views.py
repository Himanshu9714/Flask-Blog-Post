from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import Post, User, Comment
from . import db

# Creating blueprint and linked to flask app
views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    posts = Post.query.all()
    return render_template("home.html", user=current_user, posts=posts)


@views.route("/create-post", methods=["GET", "POST"])
@login_required
def create_post():
    if request.method == "POST":
        text = request.form.get("text")
        if not text:
            flash("Post can't be empty!", category="error")
        else:
            post = Post(text=text, author=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash("Post created successfully!", category="success")
            return redirect(url_for("views.home"))
    return render_template("create_post.html", user=current_user)


@views.route("/delete-post/<id>")
@login_required
def delete_post(id):
    post = Post.query.get(id)
    if not post:
        flash("Post doesn't exist!", category="error")
    elif current_user.id != post.id:
        flash("You don't have permission to delete this post!", category="error")
    else:
        db.session.delete(post)
        db.session.commit()
        flash("Post deleted!", category="success")

    return redirect(url_for("views.home"))


@views.route("/posts/<username>")
@login_required
def posts(username):
    user = User.query.filter_by(username=username).first()

    if not user:
        flash(f"No user with {username} exist!", category="error")
        return redirect(url_for("views.home"))

    posts = user.posts
    return render_template(
        "posts.html", user=current_user, posts=posts, username=username
    )


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")
    if not text:
        flash("Comment can't be empty!", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            comment = Comment(text=text, author=current_user.id, post_id=post_id)
            db.session.add(comment)
            db.session.commit()
        else:
            flash("Post doesn't exist!", category="error")

    return redirect(url_for("views.home"))


@views.route("/delete-comment/<id>")
@login_required
def delete_comment(id):
    comment = Comment.query.get(id)
    if not comment:
        flash("Comment doesn't exist!", category="error")
    elif current_user.id != comment.author and current_user.id != comment.post.id:
        flash("You don't have permission to delete this post!", category="error")
    else:
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("views.home"))
