import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://freesvg.org/img/abstract-user-flat-4.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.Text,
                           nullable=False)

    last_name = db.Column(db.Text,
                          nullable=False)

    image_url = db.Column(db.Text,
                          nullable=True,
                          default=DEFAULT_IMAGE_URL)

    posts = db.relationship("Post",
                            backref="user",
                            cascade="all, delete-orphan")


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column(db.Integer,
                   primary_key=True,)

    title = db.Column(db.Text,
                      nullable=False)

    content = db.Column(db.Text,
                        nullable=False)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'),
                        nullable=False)


class PostTag(db.Model):
    """Tag on a post."""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                        db.ForeignKey('post.id'),
                        primary_key=True)

    tag_id = db.Column(db.Integer,
                       db.ForeignKey('tag.id'),
                       primary_key=True)


class Tag(db.Model):
    """Tags to be added to a post."""

    __tablename__ = 'tag'

    id = db.Column(db.Integer,
                   primary_key=True)

    name = db.Column(db.Text,
                     nullable=False,
                     unique=True)

    posts = db.relationship('Post',
                            secondary="post_tag",
                            backref="tag",)
