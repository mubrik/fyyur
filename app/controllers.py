from datetime import datetime
from typing import List, Dict
from sqlalchemy import select, join, func
from sqlalchemy.orm import aliased
from flask import Blueprint, render_template, request, flash, redirect, url_for
from app import app, db
from .forms import VenueForm, ShowForm, ArtistForm
from .models import Artist, Venue, Show
from .forms import ArtistForm, VenueForm, ShowForm
from .utils import display_form_error

@app.route('/')
def index():
  return render_template('pages/home.html')

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  curr_datetime = datetime.now()
  # filter shows table for upcoming shows compare with curr time, group by venue and count each group
  upcoming_show_tableqry = db.session.query(Show.venue_id, func.count(Show.venue_id)\
    .label('num_upcoming_shows')).filter(Show.start_time > curr_datetime).group_by(Show.venue_id).subquery()
  # table for id name state and count upcoming shows
  venue_showcount_join = db.session.query(Venue.id, Venue.name, Venue.state, upcoming_show_tableqry.c.num_upcoming_shows)\
    .outerjoin(upcoming_show_tableqry, Venue.id == upcoming_show_tableqry.c.venue_id)\
    .group_by(Venue.state, Venue.id, Venue.name, upcoming_show_tableqry.c.num_upcoming_shows)

  # table for state group
  stmt_group_state = db.session.query(Venue.city, Venue.state).group_by(Venue.state, Venue.city)
  
  data = []
  for venue_city, venue_state in stmt_group_state:
    # wonky list comprehension but i cant figure out the best query :(
    data.append({
      "city": venue_city,
      "state": venue_state,
      "venues": [
        {"id": id, "name": name, "state": state, "num_upcoming_shows": count if count is not None else 0} 
        for id, name, state, count in venue_showcount_join
        if state == venue_state
      ]
    })
  print(data)
  if len(data) == 0:
    flash('No Venues, created yet')

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # variables
  query = request.form.get('search_term', '')
  # should bleach query?
  count = Venue.query.filter(Venue.name.ilike(f'%{query}%')).count()
  data_array = []
  # if search finds something
  if count != 0 :
    # get current date
    curr_datetime = datetime.now()
    # filter shows table for upcoming shows, group by artist and count each group
    stmt = db.session.query(Show.id, Show.venue_id, func.count('*')\
      .label('upcoming_count')).filter(Show.start_time > curr_datetime).group_by(Show.venue_id, Show.id).subquery()
    # join filtered venue table with filtered shows table
    stmt_result = db.session.query(Venue, stmt.c.upcoming_count).outerjoin(stmt, Venue.id == stmt.c.venue_id).filter(Venue.name.ilike(f'%{query}%'))
    print(stmt_result)
    for venue, show_c in stmt_result:
      data_array.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": show_c if show_c is not None else 0
      })
  else:
    # count is 0, found nothing
    flash('No venues found', 'info')

  response = {
    "count": count,
    "data": data_array
  }
  print(response)
  return render_template('pages/search_venues.html', results=response, search_term=query)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id: int):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # get artist
  venue = Venue.query.get(venue_id)
  upcoming_shows = []
  past_shows = []
  if venue is not None:
    # curr date
    current_date = datetime.now()
    # compare dates
    for show in venue.shows:
      if show.start_time > current_date:
        upcoming_shows.append({
          "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": show.start_time.isoformat() # datatetime obj
        })
      else:
        past_shows.append({
          "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": show.start_time.isoformat() # datatetime obj
        })
    data = venue
    setattr(data, "upcoming_shows", upcoming_shows)
    setattr(data, "upcoming_shows_count", upcoming_shows.__len__())
    setattr(data, "past_shows", past_shows)
    setattr(data, "past_shows_count", past_shows.__len__())
  else:
    flash('Venue does not exist')
    return render_template('pages/home.html')
  return render_template('pages/show_venue.html', venue=data)

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm(formdata=None)
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # create form to validate
  venue_form = VenueForm()
  if venue_form.validate_on_submit():
    # create Venue
    venue = Venue(venue_form.data)
    # add
    db.session.add(venue)
    # commit db session
    db.session.commit()
    try:
      # add
      db.session.add(venue)
      # commit db session
      db.session.commit()
    except:
      # if exception, wrong info form
      flash('Error, check Form')
      # render the previous form
      return render_template('forms/new_venue.html', form=VenueForm(formdata=None))
    else:
      # on successful db insert, flash success
      flash('Venue ' + venue_form.name.data + ' was successfully listed!')
  else :
    # TODO: on unsuccessful db insert, flash an error instead.
    display_form_error(venue_form.errors)
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['GET'])
def delete_venue(venue_id: int):
  return render_template('pages/delete_venue.html')

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue_submission(venue_id: int):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # get venue
  venue = Venue.query.get(venue_id)
  if venue is not None:
    db.session.delete(venue)
    res = db.session.commit()
    flash('Venue Deleted')
    return redirect(url_for('index'))
  else:
    flash('Error deleting item')
  return None

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id: int):
  # get venue
  venue = Venue.query.get(venue_id)
  if venue is not None:
    form = VenueForm(obj=venue)
  else:
    flash('Venue does not exist', 'error')
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id: int):
  # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
  # get venue
  venue = Venue.query.get(venue_id)
  # get form
  venue_form = VenueForm()
  # validate
  if venue_form.validate_on_submit():
    # loop form data
    print(venue)
    for key, val in venue_form.data.items():
      setattr(venue, key, val)
    # commit db session
    db.session.commit()
    # on successful db insert, flash success
    flash('Venue ' + venue_form.name.data + ' was successfully edited!')
  else:
    display_form_error(venue_form.errors)
  return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # get artists
  data = Artist.query.limit(100).all()

  if len(data) == 0:
    flash('No Artists have been created', 'error')
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # variables
  query = request.form.get('search_term', '')
  # should bleach query?
  count = Artist.query.filter(Artist.name.ilike(f'%{query}%')).count()
  data_array = []
  # if search finds something
  if count != 0 :
    # get current date
    curr_datetime = datetime.now()
    # filter shows table for upcoming shows, group by artist and count each group
    stmt = db.session.query(Show.artist_id, func.count('*')\
      .label('upcoming_count')).filter(Show.start_time > curr_datetime).group_by(Show.artist_id).subquery()
    # join filtered artist table with filtered shows table
    stmt_result = db.session.query(Artist, stmt.c.upcoming_count).outerjoin(stmt, Artist.id == stmt.c.artist_id).filter(Artist.name.ilike(f'%{query}%'))
    print(stmt_result)
    for artist, show_c in stmt_result:
      data_array.append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": show_c if show_c is not None else 0
      })
  else:
    # count is 0, found nothing
    flash('No artists found', 'info')

  response = {
    "count": count,
    "data": data_array
  }
  return render_template('pages/search_artists.html', results=response, search_term=query)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # get artist
  artist = Artist.query.get(artist_id)
  upcoming_shows = []
  past_shows = []
  if artist is not None:
    # curr date
    current_date = datetime.now()
    # compare dates
    for show in artist.shows:
      if show.start_time > current_date:
        upcoming_shows.append({
          "venue_id": show.venue_id,
          "venue_name": show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": show.start_time.isoformat() # datatetime obj
        })
      else:
        past_shows.append({
          "venue_id": show.venue_id,
          "venue_name": show.venue.name,
          "venue_image_link": show.venue.image_link,
          "start_time": show.start_time.isoformat() # datatetime obj
        })
    data = artist
    setattr(data, "upcoming_shows", upcoming_shows)
    setattr(data, "upcoming_shows_count", upcoming_shows.__len__())
    setattr(data, "past_shows", past_shows)
    setattr(data, "past_shows_count", past_shows.__len__())
  else:
    flash('Artist does not exist')
  return render_template('pages/show_artist.html', artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id: int):
  # get artist
  artist = Artist.query.get(artist_id)
  if artist is not None:
    form = ArtistForm(obj=artist)
    # TODO: populate form with fields from artist with ID <artist_id>
  else:
    flash('Artist does not exist', 'error')
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
  # get artist
  artist = Artist.query.get(artist_id)
  # get form
  artist_form = ArtistForm()
  # validate
  if artist_form.validate_on_submit():
    # loop form data
    print(artist)
    for key, val in artist_form.data.items():
      setattr(artist, key, val)
    # commit db session
    db.session.commit()
    # on successful db insert, flash success
    flash('Artist ' + artist_form.name.data + ' was successfully edited!')
  else:
    display_form_error(artist_form.errors)
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm(formdata=None)
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
  # create form to validate
  artist_form = ArtistForm()
  if artist_form.validate_on_submit():
    # create artist
    artist = Artist(artist_form.data)
    try:
      # add
      db.session.add(artist)
      # commit db session
      db.session.commit()
    except:
      # if exception, wrong artist/venue id
      flash('Error, check Form')
      # render the previous form
      return render_template('forms/new_artist.html', form=ArtistForm(formdata=None))
    else:
      # on successful db insert, flash success
      flash('Artist ' + artist_form.name.data + ' was successfully listed!')
  else :
    # TODO: on unsuccessful db insert, flash an error instead.
    display_form_error(artist_form.errors)
  return render_template('pages/home.html')

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  all_shows = Show.query.limit(100).all()
  data = []
  for show in all_shows:
    data.append({
      "venue_id": show.venue_id,
      "venue_name": show.venue.name,
      "artist_id": show.artist_id,
      "artist_name": show.artist.name,
      "artist_image_link": show.artist.image_link,
      "start_time": show.start_time.isoformat() # datatetime obj
    })
  
  if len(data) == 0:
    flash('No Shows have been created', 'error')
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm(formdata=None)
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create',  methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # create form to validate
  show_form = ShowForm()
  if show_form.validate_on_submit():
    # create Show
    show = Show(show_form.data)
    # add
    db.session.add(show)
    try:
      # commit db session
      db.session.commit()
    except:
      # if exception, wrong artist/venue id
      flash('Error, check Artist/Venue')
      # render the previous form
      return render_template('forms/new_show.html', form=ShowForm(formdata=None))
    else:
      # on successful db insert, flash success
      flash('Show created successfully listed!')
  else :
    # TODO: on unsuccessful db insert, flash an error instead.
    display_form_error(show_form.errors)
  return render_template('pages/home.html')

# error handlers
@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
  return render_template('errors/500.html'), 500
