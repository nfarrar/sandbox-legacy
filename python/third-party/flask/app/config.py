import os


#: Flask Application Configuration
DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = os.urandom(24)
APP_DIR = os.path.dirname(os.path.abspath(__file__))


#: Flask-SQLAlchemy extension settings
SQLALCHEMY_ECHO = True
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/flask-skeleton.db'
