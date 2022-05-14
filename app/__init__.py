from flask import Flask, render_template
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

# routes blueprint
# from .controllers import fyyur_route

# register route blueprint
# app.register_blueprint(fyyur_route), blueprint bit of work, check controllers comment
# register url to views/controller, kinda like django :)
from . import controllers
app.add_url_rule('/', view_func=controllers.index)
app.add_url_rule('/venues', view_func=controllers.venues)
app.add_url_rule('/venues/search', view_func=controllers.search_venues)
app.add_url_rule('/venues/<int:venue_id>', view_func=controllers.show_venue)
app.add_url_rule('/venues/create', view_func= controllers.create_venue_form, methods=['GET'])
app.add_url_rule('/venues/create', view_func= controllers.create_venue_submission, methods=['POST'])
app.add_url_rule('/venues/<venue_id>', view_func=controllers.delete_venue, methods=['DELETE'])
app.add_url_rule('/venues/<int:venue_id>/edit', view_func=controllers.edit_venue, methods=['GET'])
app.add_url_rule('/venues/<int:venue_id>/edit', view_func=controllers.edit_venue_submission, methods=['POST'])
app.add_url_rule('/artists', view_func= controllers.artists)
app.add_url_rule('/artists/search', view_func= controllers.search_artists, methods=['POST'])
app.add_url_rule('/artists/<int:artist_id>', view_func=controllers.show_artist )
app.add_url_rule('/artists/<int:artist_id>/edit', view_func=controllers.edit_artist ,methods=['GET'])
app.add_url_rule('/artists/<int:artist_id>/edit', view_func=controllers.edit_artist_submission, methods=['POST'])
app.add_url_rule('/artists/create', view_func=controllers.create_artist_form, methods=['GET'])
app.add_url_rule('/artists/create', view_func=controllers.create_artist_submission, methods=['POST'] )
app.add_url_rule('/shows', view_func=controllers.shows)
app.add_url_rule('/shows/create', view_func=controllers.create_shows)
app.add_url_rule('/shows/create', view_func=controllers.create_show_submission, methods=['POST'])

# error handlers
@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
  return render_template('errors/500.html'), 500

# create DB
db.create_all()
