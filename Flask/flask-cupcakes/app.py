"""Flask app for Cupcakes"""

from flask import Flask, render_template, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake

app = Flask(__name__)
app.app_context().push()

app.config["SECRET_KEY"] = "177013"
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///cupcakes"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
debug = DebugToolbarExtension(app)


connect_db(app)


def serialize_cupcake(self):
    """Serialize a cupcake."""

    return {
        "id": self.id,
        "flavor": self.flavor,
        "rating": self.rating,
        "size": self.size,
        "image": self.image,
    }


@app.route('/')
def root():

    return render_template("index.html")


@app.route("/api/cupcakes")
def list_all_cupcakes():
    """ Get data about all cupcakes.
        Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}.
    """

    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]

    return jsonify(cupcakes=cupcakes)
    # end list_cupcakes


@app.route("/api/cupcakes/<int:cupcake_id>")
def list_single_cupcake(cupcake_id):
    """ Get data about a single cupcakes.
        Respond with JSON like: {cupcake: [{id, flavor, size, rating, image}]}.
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    return jsonify(cupcake=cupcake.to_dict())
    # end list_single_cupcake


@app.route("/api/cupcakes", methods=["POST"])
def create_cupcake():
    """ Create a cupcake from form data & return it.
        Respond with JSON like: {cupcake: [{id, flavor, size, rating, image}]}.
    """
    data = request.json

    cupcake = Cupcake(
        flavor = request.json["flavor"],
        size = request.json["size"],
        rating = request.json["rating"],
        image = request.json["image"] or None)

    db.session.add(cupcake)
    db.session.commit()

    # Return w/status code 201 --- return tuple (json, status)
    return (jsonify(cupcake=cupcake.to_dict()), 201)
    # end create_cupcake


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["PATCH"])
def update_cupcake(cupcake_id):
    """ Update a cupcake with the id passed in the URL.
        Respond with JSON of the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating, image}}.
    """

    data = request.json

    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size',  cupcake.size)
    cupcake.rating = request.json.get('rating',  cupcake.rating)
    cupcake.image = request.json.get('image',  cupcake.image)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=cupcake.to_dict())
    # end update_cupcake


@app.route("/api/cupcakes/<int:cupcake_id>", methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """ Delete cupcake with the id passed in the URL.
        Respond with JSON like {message: "Deleted"}.
    """

    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message="Deleted")
    # end delete_cupcake