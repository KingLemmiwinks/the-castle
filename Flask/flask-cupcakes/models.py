"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://thestayathomechef.com/wp-content/uploads/2017/12/Most-Amazing-Chocolate-Cupcakes-1-small.jpg"

# Models
class Cupcake(db.Model):
    """Cupcake."""
    __tablename__ = 'cupcake'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    flavor = db.Column(db.Text,
                           nullable=False)

    size = db.Column(db.Text,
                          nullable=False)

    rating = db.Column(db.Float,
                          nullable=False)

    image = db.Column(db.Text,
                      nullable=False,
                      default=DEFAULT_IMAGE_URL)

    def to_dict(self):
        """Serialize a cupcake to a dict."""

        return {
            "id": self.id,
            "flavor": self.flavor,
            "rating": self.rating,
            "size": self.size,
            "image": self.image,
        }

# Connect to database
def connect_db(app):
    """Connect to the database."""
    db.app = app
    db.init_app(app)
