from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    """user_table"""

    # Unique id for each user
    id = db.Column(db.Integer, primary_key=True)

    # Unique email per each user
    email = db.Column(db.String(150), unique=True)

    # Unique username per each user
    username = db.Column(db.String(150), unique=True)

    # Password for the user
    password = db.Column(db.String(150))

    # Date creation for user
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # Backref is used to get user's posts and comments
    # For eg, user.posts: Gives all posts related to user
    posts = db.relationship("Post", backref="user", passive_deletes=True)

    # user.comments: Gives all comments related to user
    comments = db.relationship("Comment", backref="user", passive_deletes=True)

    # user.likes: Gives all likes related to user
    likes = db.relationship("Like", backref="user", passive_deletes=True)


class Post(db.Model):
    """post_table"""

    # Unique id for each post
    id = db.Column(db.Integer, primary_key=True)

    # Content of the post
    text = db.Column(db.Text, nullable=False)

    # Date creation for the post
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # One to many relation from user to post
    # A user can have multiple posts
    author = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # post.comments: Gives all comments related to post
    comments = db.relationship("Comment", backref="post", passive_deletes=True)

    # post.likes: Gives all likes related to post
    likes = db.relationship("Like", backref="post", passive_deletes=True)


class Comment(db.Model):
    """comment_table"""

    # Unique id for each comment
    id = db.Column(db.Integer, primary_key=True)

    # Content of the comment
    text = db.Column(db.String(200), nullable=False)

    # Date creation for the comment
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())

    # One to many relationship from user to comments
    # A user can have multiple comments on different posts
    author = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # One to many relationship from post to comments
    # A post can have multiple comments
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )


class Like(db.Model):
    """like_table"""

    # Unique id for each comment
    id = db.Column(db.Integer, primary_key=True)

    # One to many relationship from user to like
    # A user can have multiple likes on different posts
    author = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )

    # One to many relationship from post to like
    # A post can have multiple likes
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )