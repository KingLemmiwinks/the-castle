"""Capstone 1"""

import requests, json
from flask import Flask, request, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from forms import RegisterForm, LoginForm
from models import db, connect_db, User, Likes
from sqlalchemy.exc import IntegrityError

API_BASE_URL = "https://www.dnd5eapi.co/api"
CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///capstone_1_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "177013"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


############################## HOME ROUTE ##############################

@app.route('/')
def home():
    """Show home page."""

    return render_template('index.html')


############################## USER ROUTES ##############################


def do_login(user):
    """Login user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr_user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


@app.route("/register", methods=["GET", "POST"])
def register():
    """Produce register form and handle form submission."""

    if g.user:
        flash("You Are Already Registered.", "danger")
        return redirect("/")

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            name = form.username.data,
            pwd = form.password.data

            user = User.register(name, pwd)
            db.session.add(user)
            db.session.commit()

        except IntegrityError as e:
            flash("Username already taken", 'danger')
            return render_template('register.html', form=form)


        do_login(user)
        session["user_id"] = user.id

        flash("You are now registered!", "success")
        return redirect("/spells")

    else:
        return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form and handle form submission."""

    if g.user:
        flash("You Are Already Logged In.", "danger")
        return redirect("/")

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        user = User.authenticate(name, pwd)

        if user:
            do_login(user)
            session["user_id"] = user.id  # keep logged in
            return redirect("/")

        else:
            form.username.errors = ["Bad name/password"]

    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    """Handle user logout."""

    if not g.user:
        flash("You Are Not Logged In.", "danger")
        return redirect("/")

    do_logout()
    flash('You have been logged out.', 'success')
    return redirect("/login")


############################## SPELL ROUTES ##############################


def get_all_spells():
    """Call the API for all spells."""

    api_url = f"{API_BASE_URL}/spells"
    response = requests.get(api_url)

    spells = (response.json()['results'])

    return spells

def get_spell_detail(index):
    """Call the API for a spell index."""

    api_url = f"{API_BASE_URL}/spells/{index}"
    response = requests.get(api_url)

    spell_detail = (response.json())

    return spell_detail

@app.route('/spells')
def get_all_spells_page():
    """Shows all spells on the screen."""

    if not g.user:
        flash("Please Login or Register to view spells.", "danger")
        return redirect("/")

    spells = get_all_spells()
    
    liked_spells = [like.spell_index for like in g.user.likes]
    
    return render_template('index.html', spells=spells, likes=liked_spells)


@app.route('/spells/<index>')
def get_spell_detail_page(index):
    """Shows details about an individual spell."""

    if not g.user:
        flash("Please Login or Register to view spell details.", "danger")
        return redirect("/")

    spell_detail = get_spell_detail(index)

    return render_template('spell_detail.html', spell_detail=spell_detail)


@app.route('/spells/<string:spell_index>/<string:spell_name>/like', methods=['POST'])
def add_like(spell_index, spell_name):
    """Toggle a current user's favorite spell."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user_likes = g.user.likes

    liked_spell_index = Likes.query.filter(
        Likes.spell_index == spell_index).first()

    if liked_spell_index in user_likes:
        # Unfavorite
        remove_like_from_db(spell_index)

    else:
        # Favorite a spell        
        add_like_to_db(spell_index, spell_name)
        

    return redirect("/spells")


############################## FAVORITES ROUTES ##############################


def add_like_to_db(spell_index, spell_name):
    """Build row data and add spell to likes table"""
    new_like = Likes()
    new_like.spell_index = spell_index
    new_like.user_id = g.user.id
    new_like.spell_name = spell_name

    g.user.likes.append(new_like)

    db.session.commit()


def remove_like_from_db(spell_index):
    """Search for the liked spell index from the current user and remove the like."""
    Likes.query.filter(Likes.user_id == g.user.id,
                       Likes.spell_index == spell_index).delete()

    db.session.commit()


@app.route('/favorites')
def put_favorites_on_page():
    """Show all current user's favorite spells."""

    if not g.user:
        flash("Please Login or Register to view favorites.", "danger")
        return redirect("/")

    spells = get_all_spells()

    liked_spells = [like for like in g.user.likes]

    return render_template('favorites.html', likes=g.user.likes)


@app.route('/favorites/<string:spell_index>/remove', methods=['POST'])
def remove_favorite(spell_index):
    """Remove favorite spell from the favorites page."""

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    remove_like_from_db(spell_index)

    return redirect("/favorites")



