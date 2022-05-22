'''
  contains the route handlers for various endpoint
'''
from datetime import datetime
from typing import List
from sqlalchemy import func
from flask import (
  render_template, request, flash,
  redirect, url_for, jsonify
)
from app import app, db
from .forms import VenueForm, ShowForm, ArtistForm, AlbumForm, SongForm
from .models import Artist, Venue, Show, Album, Song
from .utils import display_form_error


@app.route('/index')
@app.route('/')
def index():
  recent_venues = Venue.query.order_by(Venue.date_created).all()
  recent_artists = Artist.query.order_by(Artist.date_created).all()
  data = {
    "artists": recent_artists,
    "venues": recent_venues
  }
  return render_template('pages/home.html', data=data)


@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  # curr_datetime = datetime.now()
  # # filter shows table for upcoming shows compare with curr time, group by venue and count each group
  # upcoming_show_tableqry = db.session.query(Show.venue_id, func.count(Show.venue_id)\
  #   .label('num_upcoming_shows')).filter(Show.start_time > curr_datetime).group_by(Show.venue_id).subquery()
  # # table for id name state and count upcoming shows
  # venue_showcount_join = db.session.query(Venue.id, Venue.name, Venue.state, upcoming_show_tableqry.c.num_upcoming_shows)\
  #   .outerjoin(upcoming_show_tableqry, Venue.id == upcoming_show_tableqry.c.venue_id)\
  #   .group_by(Venue.state, Venue.id, Venue.name, upcoming_show_tableqry.c.num_upcoming_shows)

  # # table for state grouping, distinct by state
  # stmt_group_state = db.session.query(Venue.city, Venue.state).distinct(Venue.state)
  # print(stmt_group_state)
  
  # data = []
  # for venue_city, venue_state in stmt_group_state:
  #   data.append({
  #     "city": venue_city,
  #     "state": venue_state,
  #     # wonky list comprehension but i cant figure out the best query :( yet
  #     "venues": [
  #       {"id": id, "name": name, "state": state, "num_upcoming_shows": count if count is not None else 0} 
  #       for id, name, state, count in venue_showcount_join
  #       if state == venue_state
  #     ]
  #   })
  # print(data)
  
  distinct_venues: List[Venue] = Venue.query.distinct(Venue.state, Venue.city).all()
  all_venues: List[Venue] = Venue.query.all()
  returned_data = []
  curr_datetime = datetime.now()
  
  for venue in distinct_venues:
    returned_data.append({
      "city": venue.city,
      "state": venue.state,
      "venues": [
        {"id": sub_venue.id, "name": sub_venue.name, 
         "state": sub_venue.state, 
         "num_upcoming_shows": len([show for show in sub_venue.shows if show.start_time > curr_datetime])
        }
        for sub_venue in all_venues
        if sub_venue.city == venue.city and sub_venue.state == venue.state
      ]
    })

  if len(returned_data) == 0:
    flash('No Venues, created yet')

  return render_template('pages/venues.html', areas=returned_data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
  # variables
  query = request.form.get('search_term', '')
  # should bleach query?
  venues_query: List[Venue] = Venue.query.filter(Venue.name.ilike(f'%{query}%')).all()
  data_array = []
  # time
  curr_datetime = datetime.now()
  if len(venues_query) > 0:
    # shows is joined iin relationship
    for venue in venues_query:
      data_array.append({
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": len([
          show for show in venue.shows
          if show.start_time >= curr_datetime
        ])
      })
  # data_array = []
  # # if search finds something
  # if count != 0 :
  #   # get current date
  #   curr_datetime = datetime.now()
  #   # 
  #   # filter shows table for upcoming shows, group by artist and count each group
  #   stmt = db.session.query(Show.id, Show.venue_id, func.count('*')\
  #     .label('upcoming_count')).filter(Show.start_time > curr_datetime).group_by(Show.venue_id, Show.id).subquery()
  #   # join filtered venue table with filtered shows table
  #   stmt_result = db.session.query(Venue, stmt.c.upcoming_count).outerjoin(stmt, Venue.id == stmt.c.venue_id).filter(Venue.name.ilike(f'%{query}%'))
  #   print(stmt_result)
  #   for venue, show_c in stmt_result:
  #     data_array.append({
  #       "id": venue.id,
  #       "name": venue.name,
  #       "num_upcoming_shows": show_c if show_c is not None else 0
  #     })
  else:
    # count is 0, found nothing
    flash('No venues found', 'info')

  response = {
    "count": len(venues_query),
    "data": data_array
  }
  print(response)
  return render_template('pages/search_venues.html', results=response, search_term=query)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id: int):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  # get venue
  venue: Venue = Venue.query.get(venue_id)
  upcoming_shows = []
  past_shows = []
  if venue is not None:
    # get time
    curr_time = datetime.now()
    # show is a joined query iterate
    for show in venue.shows:
      show_obj = {
        "artist_id": show.artist_id, 
        "artist_name": show.artist.name, 
        "artist_image_link": show.artist.website_link, 
        "start_time": show.start_time
      }
      
      if (show.start_time >= curr_time):
        upcoming_shows.append(show_obj)
      else:
        past_shows.append(show_obj)
  
    data = vars(venue)
    data['upcoming_shows'] = upcoming_shows
    data['upcoming_shows_count'] = len(upcoming_shows)
    data['past_shows'] = past_shows
    data['past_shows_count'] = len(past_shows)
    # query, filter by start date and artist id, join on artistid
    # upcoming_shows_query = db.session.query(Show.start_time, Artist.id, Artist.name, Artist.image_link)\
    #   .filter(Show.venue_id == venue_id).filter(Show.start_time > datetime.now()).join(Artist, Show.artist_id == Artist.id)
    # past_shows_query = db.session.query(Show.start_time, Artist.id, Artist.name, Artist.image_link)\
    #   .filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).join(Artist, Show.artist_id == Artist.id)
    # # counts
    # upcoming_shows_count = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time >  curr_time).count()
    # past_shows_count = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time <  curr_time).count()
    # upcoming_shows = [
    #   {"artist_id": id, "artist_name": name, "artist_image_link": link, "start_time": time} 
    #   for time, id, name, link in upcoming_shows_query
    # ]

    # past_shows = [
    #   {"artist_id": id, "artist_name": name, "artist_image_link": link, "start_time": time} 
    #   for time, id, name, link in past_shows_query
    # ]
    # data = venue
    # print(data.website_link)
    # setattr(data, "upcoming_shows", upcoming_shows)
    # setattr(data, "upcoming_shows_count", upcoming_shows_count)
    # setattr(data, "past_shows", past_shows)
    # setattr(data, "past_shows_count", past_shows.__len__())
  else:
    flash('Venue does not exist')
    return redirect(url_for('venues'))
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
      # rollback
      db.session.rollback()
      # render the previous form
      return render_template('forms/new_venue.html', form=VenueForm(formdata=None))
    else:
      # on successful db insert, flash success
      flash('Venue ' + venue_form.name.data + ' was successfully listed!')
    finally:
      db.session.close()
  else :
    # TODO: on unsuccessful db insert, flash an error instead.
    display_form_error(venue_form.errors)
  return redirect(url_for('index'))

# @app.route('/venues/<venue_id>/delete', methods=['GET'])
# def delete_venue(venue_id: int):
#   return render_template('pages/delete_venue.html')

@app.route('/venues/<venue_id>/delete', methods=['POST'])
def delete_venue_submission(venue_id: int):
  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  # get venue
  venue = Venue.query.get(venue_id)
  isErrored = False
  if venue is not None:
    db.session.delete(venue)
    try:
      db.session.commit()
    except:
      isErrored = True
    finally:
      db.session.close()
      if isErrored:
        flash('Error deleting item')
        return jsonify({"status": "fail", "message": "Venue not found"});
      else:
        flash('Venue Deleted')
        return jsonify({"status": "success", "message": "Completed"});
  else:
    flash('Error deleting item')
    return jsonify({"status": "fail", "message": "Venue not found"});

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
    try:
      # commit db session
      db.session.commit()
      # on successful db insert, flash success
      flash('Venue ' + venue_form.name.data + ' was successfully edited!')
    except:
      flash('Error editing venue')
      db.session.rollback()
    finally:
      db.session.close()
  else:
    display_form_error(venue_form.errors)
  return redirect(url_for('show_venue', venue_id=venue_id))

@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database
  # get artists
  artists_query: List[Artist] = Artist.query.limit(100).all()
  data = []
  # time
  curr_datetime = datetime.now()
  if len(artists_query) == 0:
    flash('No Artists have been created', 'error')
  else:
    for artist in artists_query:
      temp_artist = vars(artist)
      temp_artist["num_upcoming_shows"] = len([
        show for show in artist.shows
        if show.start_time > curr_datetime
      ])
      data.append(temp_artist)

  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # variables
  query = request.form.get('search_term', '')
  # should bleach query?
  artists_query = Artist.query.filter(Artist.name.ilike(f'%{query}%')).all()
  data_array = []
  curr_datetime = datetime.now()
  if len(artists_query) > 0:
    # shows is joined iin relationship
    for artist in artists_query:
      data_array.append({
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": len([
          show for show in artist.shows
          if show.start_time >= curr_datetime
        ])
      })
  else:
    # count is 0, found nothing
    flash('No artists found', 'info')

  response = {
    "count": len(artists_query),
    "data": data_array
  }
  return render_template('pages/search_artists.html', results=response, search_term=query)

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  # get artist
  artist: Artist = Artist.query.get(artist_id)
  upcoming_shows = []
  past_shows = []
  if artist is not None:
    # curr date
    curr_time = datetime.now()
    # iterate outer joined shows
    for show in artist.shows:
      artist_obj = {
        "venue_id": show.venue_id, 
        "venue_name": show.venue.name, 
        "venue_image_link": show.venue.website_link, 
        "start_time": show.start_time
      }
      
      if (show.start_time >= curr_time):
        upcoming_shows.append(artist_obj)
      else:
        past_shows.append(artist_obj)
  
    data = vars(artist)
    data['upcoming_shows'] = upcoming_shows
    data['upcoming_shows_count'] = len(upcoming_shows)
    data['past_shows'] = past_shows
    data['past_shows_count'] = len(past_shows)

    # query, filter by start date and artist id
    # upcoming_shows_query = db.session.query(Show.start_time, Venue.id, Venue.name, Venue.image_link)\
    #   .filter(Show.artist_id == artist_id).filter(Show.start_time > datetime.now()).join(Venue, Show.venue_id == Venue.id)
    # past_shows_query = db.session.query(Show.start_time, Venue.id, Venue.name, Venue.image_link)\
    #   .filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).join(Venue, Show.venue_id == Venue.id)
    # # counts
    # upcoming_shows_count = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time >  curr_time).count()
    # past_shows_count = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time <  curr_time).count()
    
    # upcoming_shows = [
    #   {"venue_id": id, "venue_name": name, "venue_image_link": link, "start_time": time} 
    #   for time, id, name, link in upcoming_shows_query
    # ]

    # past_shows = [
    #   {"venue_id": id, "venue_name": name, "venue_image_link": link, "start_time": time} 
    #   for time, id, name, link in past_shows_query
    # ]

    # data = artist
    # setattr(data, "upcoming_shows", upcoming_shows)
    # setattr(data, "upcoming_shows_count", upcoming_shows_count)
    # setattr(data, "past_shows", past_shows)
    # setattr(data, "past_shows_count", past_shows_count)
  else:
    flash('Artist does not exist')
    return redirect(url_for("artists"))
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
    for key, val in artist_form.data.items():
      # should bleach some keys
      setattr(artist, key, val)
    try:
      # commit db session
      db.session.commit()
      # on successful db insert, flash success
      flash('Artist ' + artist_form.name.data + ' was successfully edited!')
    except:
      db.session.rollback()
      flash('Error editing Artist')
    finally:
      db.session.close()
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
      return render_template('forms/new_artist.html', form=ArtistForm(data=artist_form.data))
    else:
      # on successful db insert, flash success
      flash('Artist ' + artist_form.name.data + ' was successfully listed!')
    finally:
      db.session.close()
  else :
    # TODO: on unsuccessful db insert, flash an error instead.
    display_form_error(artist_form.errors)
    return render_template('forms/new_artist.html', form=ArtistForm(data=artist_form.data))
  return redirect(url_for('index'))

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

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead
  # create form to validate
  show_form = ShowForm()
  if show_form.validate_on_submit():
    # implement time availabilty, cant boo a show in same day already booked show
     # get artist nd time
    artist_id: int = show_form.artist_id.data
    start_time: datetime = show_form.start_time.data
    # get upcoming show with same date
    upcoming_show = Show.query.filter(Show.artist_id == artist_id).filter(func.date(Show.start_time) == start_time.date()).first()
    if upcoming_show is not None:
      # that means show with date exist, return
      flash('Error, Artist has a show scheduled for this date')
      # render the previous form
      return render_template('forms/new_show.html', form=ShowForm(data=show_form.data))
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
      return render_template('forms/new_show.html', form=ShowForm(data=show_form.data))
    else:
      # on successful db insert, flash success
      flash('Show created successfully listed!')
    finally:
      db.session.close()
  else :
    # TODO: on unsuccessful db insert, flash an error instead.
    display_form_error(show_form.errors)
  return redirect(url_for('index'))

@app.route('/songs/create')
def create_song():
  form = SongForm(formdata=None)
  return render_template('forms/new_song.html', form=form)

@app.route('/songs/create', methods=['POST'])
def create_song_submission():
  # form data
  song_form = SongForm()
  # logic
  if song_form.validate_on_submit():
    # verify artist and album
    artist = Artist.query.get(song_form.artist_id.data)
    # this way, the album must be for the artist as well
    album = Album.query.filter(Album.id == song_form.album_id.data).filter(Album.artist_id == song_form.artist_id.data).first()

    if artist is None:
      # error, return
      flash('Error artist doesnt exist, Check artist ID')
      return render_template('forms/new_song.html', form=SongForm(data=song_form.data))
    if album is None:
      # seperate if checks for better ux
      flash('Error, Check Album ID. Artist has no album of that ID')
      return render_template('forms/new_song.html', form=SongForm(data=song_form.data))
    # artist and album fine
    song = Song(song_form.data)
    # add
    db.session.add(song)
    try:
      # commit db session
      db.session.commit()
    except:
      # if exception, wrong artist/venue id
      flash('Error, check Artist/Album')
      # render the previous form
      return render_template('forms/new_song.html', form=SongForm(data=song_form.data))
    else:
      # on successful db insert, flash success
      flash('Song successfully listed!')
    finally:
      db.session.close()
  else:
    display_form_error(song_form.errors)
    return render_template('forms/new_song.html', form=SongForm(data=song_form.data))
  
  return redirect(url_for('index'))

@app.route('/albums/create')
def create_album():
  form = AlbumForm(formdata=None)
  return render_template('forms/new_album.html', form=form)

@app.route('/albums/create', methods=['POST'])
def create_album_submission():
  # form data
  album_form = AlbumForm()
  # logic
  if album_form.validate_on_submit():
    # verify artist
    artist = Artist.query.get(album_form.artist_id.data)
    if artist is None:
      # error, return
      flash('Error, Check artistid')
      return render_template('forms/new_album.html', form=AlbumForm(data=album_form.data))
    # verify album name hasnt been created
    created_album = Album.query.filter(Album.artist_id == album_form.artist_id.data).filter(Album.name == album_form.data).first()
    if created_album is not None:
      flash('Error, Album with that name exist for the artist')
      return render_template('forms/new_album.html', form=AlbumForm(data=album_form.data))
    # artist and album name fine
    album = Album(album_form.data)
    # add
    db.session.add(album)
    try:
      # commit db session
      db.session.commit()
    except:
      # if exception, wrong artist/venue id
      flash('Error, check Artist')
      # rollb
      db.session.rollback()
      # render the previous form
      return render_template('forms/new_album.html', form=AlbumForm(data=album_form.data))
    else:
      # on successful db insert, flash success
      flash('Album successfully listed!')
    finally:
      db.session.close()
  else:
    display_form_error(album_form.errors)
    return render_template('forms/new_album.html', form=AlbumForm(data=album_form.data))
  
  return redirect(url_for('index'))

@app.route('/tracks')
def tracks():
  # get songs and albums
  songs = Song.query.all()
  albums = Album.query.all()
  return render_template('pages/tracks.html', data={"songs": songs, "albums": albums})

# error handlers
@app.errorhandler(404)
def not_found_error(error):
  return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
  return render_template('errors/500.html'), 500
