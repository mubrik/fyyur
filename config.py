import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# TODO IMPLEMENT DATABASE URL
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mubrik:postgres@localhost/fyyur_db'
# 2 cores
THREADS_PER_PAGE = 2

SECRET_KEY = os.urandom(32)

# for flask-wtfforms csrf, csrf isnt in html template,removing so forms validate fine
WTF_CSRF_ENABLED = False