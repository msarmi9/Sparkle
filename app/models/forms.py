"""
Forms for registering doctors, patients, and prescriptions.
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import FileField
from wtforms import IntegerField
from wtforms import PasswordField
from wtforms import StringField
from wtforms import SubmitField
from wtforms.validators import DataRequired


class InfoForm(FlaskForm):
    """Base class for registering names and email."""

    firstname = StringField("First name", validators=[DataRequired()])
    lastname = StringField("Last name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])


class UserForm(FlaskForm):
    """Base class for registering a username and password."""

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])


class RegistrationForm(InfoForm, UserForm):
    """Final class for registering new users (doctors)."""

    submit = SubmitField("Submit")


class LoginForm(UserForm):
    """Final class for logging in existing users (doctors)."""

    submit = SubmitField("Login")


class PatientForm(InfoForm):
    """Final class for registering new patients."""

    age = IntegerField("Age", validators=[DataRequired()])
    weight = IntegerField("Weight", validators=[DataRequired()])


class PrescriptionForm(FlaskForm):
    """Form for creating new prescriptions."""

    # TODO: We technically don't need these wtf/Flask forms.
    #       The only reason why we have them now is to provide the CSRF token
    #       to the frontend/templates when rendering the form.
    #       At least one field is needed for this FlaskForm so
    #       that's why `drug` is still here.
    drug = StringField("Drug name", validators=[DataRequired()])


class UploadFileForm(FlaskForm):
    """Form to upload a file."""

    file_selector = FileField("File", validators=[FileRequired()])
    submit = SubmitField("Submit")
