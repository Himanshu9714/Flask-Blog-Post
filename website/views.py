from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from .models import Post, User, Comment, Like
from . import db

# Creating blueprint and linked to flask app
views = Blueprint("views", __name__)


@views.route("/")
@views.route("/home")
def home():
    # Get all posts from all users
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
            # Create a post
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
    # Check if post exist
    if not post:
        flash("Post doesn't exist!", category="error")
    elif current_user.id != post.id:
        flash("You don't have permission to delete this post!", category="error")
    else:
        # Delete the post
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

    # Can get all the posts related to the logged in user via user.posts, 
    # as one to many relationship is there between post and user, and backref
    # is user to get all the posts
    posts = user.posts
    return render_template(
        "posts.html", user=current_user, posts=posts, username=username
    )


@views.route("/create-comment/<post_id>", methods=["POST"])
@login_required
def create_comment(post_id):
    text = request.form.get("text")
    # Check if comment is empty
    if not text:
        flash("Comment can't be empty!", category="error")
    else:
        post = Post.query.filter_by(id=post_id)
        if post:
            # Create a comment
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
    # Check if comment and post is of current user
    elif current_user.id != comment.author and current_user.id != comment.post.id:
        flash("You don't have permission to delete this post!", category="error")
    else:
        # The logged in user is allowed to delete the comments of post created by him. 
        # And comments which he made on other posts.
        db.session.delete(comment)
        db.session.commit()

    return redirect(url_for("views.home"))


@views.route("/like-post/<post_id>", methods=["POST"])
@login_required
def like(post_id):
    post = Post.query.get(post_id)
    like = Like.query.filter_by(author=current_user.id, post_id=post_id).first()
    
    # Check if post exist
    if not post:
        return jsonify({"error": "Post doesn't exist!"}, 404)
    
    # If user has already liked the post, delete the like
    elif like:
        db.session.delete(like)
        db.session.commit()

    # If user has not like the post, create a like
    else:
        like = Like(author=current_user.id, post_id=post_id)
        db.session.add(like)
        db.session.commit()
    
    return jsonify({"likes": len(post.likes), "liked": current_user.id in map(lambda x: x.author, post.likes)})
