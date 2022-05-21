from flask import Flask
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# WSGI obj
app = Flask(__name__)
moment = Moment(app)

# configs
app.config.from_object('config')

#db
db = SQLAlchemy(app)

# support migration on model changes
migrate = Migrate(app, db)

# importing controllers so the routes are registered, import late to avoid circular imports
from . import controllers

# create DB
# db.create_all()
