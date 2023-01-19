"""Blogly application."""

from flask import Flask, request, render_template,  redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "177013"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    """Homepage redirects to users"""
    return redirect('/users')


@app.route('/users')
def users():
    """Shows list of all users in db"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users.html', users=users)


@app.route('/users/create-new', methods=["GET"])
def create_user():
    """Show a form to create a new user"""
    return render_template('create_user.html')


@app.route("/users/create-new", methods=["POST"])
def users_new():
    """Handle form submission for creating a new user"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>')
def users_detail(user_id):
    """Show a page with info on a specific user"""
    user = User.query.get_or_404(user_id)
    return render_template('user_detail.html', user=user)


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """Show a form to edit an existing user"""
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def users_update(user_id):
    """Handle form submission for updating an existing user"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect("/users")
