from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import SignupForm, LoginForm, DeleteForm, FeedbackForm
from sqlalchemy.exc import IntegrityError
from werkzeug.exceptions import Unauthorized

app = Flask(__name__)
app.app_context().push()

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///flask_feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "177013"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)
app.app_context().push()

toolbar = DebugToolbarExtension(app)


@app.route('/', methods=['GET'])
def homepage():
    """Homepage that redirects to register."""

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """Register a new user with a form."""

    form = SignupForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            form.username.errors.append('Username unavailable.  Please pick another')
            return render_template('register.html', form=form)
        session['username'] = new_user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f"/{new_user.username}")

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():
    """Log a user in with a form."""

    if 'username' in session:
        return redirect(f"/{session['username']}")

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f"/{session['username']}")
        else:
            form.username.errors = ['Invalid username/password.']
            return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    """Log a user out."""

    session.pop('username')
    flash('Goodbye!', "info")
    return redirect('/login')


@app.route('/<username>')
def show_user(username):
    """Page with user details."""

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username)
    form = DeleteForm()

    return render_template('user_details.html', user=user, form=form)


@app.route('/<username>/feedback/new', methods=['GET', 'POST'])
def new_feedback(username):
    """Show add-feedback form and process it."""

    if 'username' not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()

    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        feedback = Feedback(
            title=title,
            content=content,
            username=username,
        )

        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/{feedback.username}")

    else:
        return render_template('new.html', form=form)


@app.route('/<int:feedback_id>/update', methods=['GET', 'POST'])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""

    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)

    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data

        db.session.commit()

        return redirect(f"/{feedback.username}")

    return render_template('edit.html', form=form, feedback=feedback)


@app.route('/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete feedback."""

    feedback = Feedback.query.get(feedback_id)
    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/{feedback.username}")
