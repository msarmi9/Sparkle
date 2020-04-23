import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.urandom(33)
    SQLALCHEMY_DATABASE_URI = "postgresql://root:sparkleandshine@sparkle-042220.cpika6vye4g6.us-west-2.rds.amazonaws.com/postgres"
    SQLALCHEMY_TRACK_MODIFICATIONS = True
