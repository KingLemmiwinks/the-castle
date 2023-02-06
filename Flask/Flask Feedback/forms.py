from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Length


class SignupForm(FlaskForm):
    """Signup form"""
    
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = StringField("Email", validators=[InputRequired()])
    first_name = StringField("First Name", validators=[InputRequired()])
    last_name = StringField("Last Name", validators=[InputRequired()])


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField("Username",validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField("Password",validators=[InputRequired(), Length(min=6, max=55)])


class FeedbackForm(FlaskForm):
    """Feedback form."""

    title = StringField("Title", validators=[InputRequired(), Length(max=100)])
    content = StringField("Content", validators=[InputRequired()])


class DeleteForm(FlaskForm):
    """Delete form."""
