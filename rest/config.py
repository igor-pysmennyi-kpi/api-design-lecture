import os

basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:dummypassword@postgres:5432/postgres'
SQLALCHEMY_TRACK_MODIFICATIONS = False
