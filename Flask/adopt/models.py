from flask_sqlalchemy import SQLAlchemy

default_image = "https://images.yaoota.com/Zn1GtntKyaVe2hIrp27tRTEJADM=/trim/yaootaweb-production-ke/media/crawledproductimages/1ac8a519b7edd9932fadcc9dea2d1eeb42af81bd.jpg"

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)


class Pet(db.Model):
    """Pet Model"""

    __tablename__ = 'pet'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    name = db.Column(db.Text,
                     nullable=False)

    species = db.Column(db.Text,
                        nullable=False)

    photo_url = db.Column(db.Text)

    age = db.Column(db.Integer)

    notes = db.Column(db.Text)

    available = db.Column(db.Boolean,
                          nullable=False,
                          default=True)

    def image_url(self):
        """Return image of pet"""

        return self.photo_url or default_image