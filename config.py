import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.urandom(33)
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'sparkle.db')
    # SQLALCHEMY_DATABASE_URI = 'postgresql://root:sparkisfun@sparkle.cpika6vye4g6.us-west-2.rds.amazonaws.com/postgres'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
