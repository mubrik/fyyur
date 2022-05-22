'''
 holds configs for flask ap
'''
import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))
# Enable debug mode.
DEBUG = True
# SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://mubrik:postgres@localhost/fyyur_db'
# print queries
SQLALCHEMY_ECHO = True
# 2 cores
THREADS_PER_PAGE = 2
# over head
SQLALCHEMY_TRACK_MODIFICATIONS = False
# secret key
SECRET_KEY = os.urandom(32)
# for flask-wtfforms csrf, csrf isnt in html template,removing so forms validate fine
WTF_CSRF_ENABLED = False
