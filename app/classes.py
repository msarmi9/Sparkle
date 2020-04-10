from flask_wtf import FlaskForm
from flask_login import UserMixin
from flask_wtf.file import FileRequired
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import FileField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from app import db, login_manager


class User(db.Model, UserMixin):
    """
    Represents the "User" schema for SQLAlchemy.
    Hashes the password for security.
    Using __table_args__ due to recommendation here:
    https://stackoverflow.com/questions/37908767/
        table-roles-users-is-already-defined-for-this-metadata-instance
    """
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        """
        Automatically hash password upon call of __init__()
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Verify credentials of user by comparing
        password with encoded password hash
        """
        return check_password_hash(self.password_hash, password)


class RegistrationForm(FlaskForm):
    """
    Flask form allowing users to register to our site.
    """
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class LogInForm(FlaskForm):
    """
    Flask form allowing users to log in to our site.
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class UploadFileForm(FlaskForm):
    """
    Flask form allowing users to upload a file to our site.
    """
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')


db.create_all()
db.session.commit()

# user_loader :
# This callback is used to reload the user object
# from the user ID stored in the session.
@login_manager.user_loader
def load_user(id):
    """
    Reloads the user object from the session.
    """
    return User.query.get(int(id))
