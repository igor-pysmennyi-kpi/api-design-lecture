import os

SECRET_KEY = 12345678
basedir = os.path.abspath(os.path.dirname(__file__))
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'localhost:5432'
SQLALCHEMY_TRACK_MODIFICATIONS = False
