from flask_wtf import FlaskForm
from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired

from app import db, login_manager

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LogInForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadFileForm(FlaskForm):
    file_selector = FileField('File', validators=[FileRequired()])
    submit = SubmitField('Submit')

db.create_all()
db.session.commit()

# user_loader :
# This callback is used to reload the user object
# from the user ID stored in the session.
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
