from flask_sqlalchemy import SQLAlchemy

DEFAULT_IMAGE_URL = "https://freesvg.org/img/abstract-user-flat-4.png"

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(25),
                           nullable=False)

    last_name = db.Column(db.String(25),
                          nullable=False)

    image_url = db.Column(db.Text,
                          nullable=True,
                          default=DEFAULT_IMAGE_URL)
