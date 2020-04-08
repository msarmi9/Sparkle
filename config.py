import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.urandom(33)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sparkle.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = True # flask-login uses sessions which require a secret Key
