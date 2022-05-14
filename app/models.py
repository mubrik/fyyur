from app import db

class Venue(db.Model):
  '''
  Venue model Class
  '''
  __tablename__ = 'venue'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
  seeking_description = db.Column(db.String(500))
  shows = db.relationship('Show', backref=db.backref('venue', lazy=True), lazy=True)
  genres = db.relationship('Genre', backref=db.backref('venues', lazy=True), lazy='subquery')

  def __repr__(self):
    return f"Venue(id={self.id!r}, name={self.name!r})"

class Artist(db.Model):
  '''
  Artist model Class
  '''
  __tablename__ = 'artist'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  genres = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
  shows = db.relationship('Show', backref=db.backref('artist', lazy=True), lazy=True)
  genres = db.relationship('Genre', backref=db.backref('artists', lazy=True), lazy='subquery')

  def __repr__(self):
    return f"Artist(id={self.id!r}, name={self.name!r})"

class Show(db.Model):
  '''
  Show model Class
  '''
  __tablename__ = 'show'

  id = db.Column(db.Integer, primary_key=True)
  start_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)

  def __repr__(self):
    return f"Show(id={self.id!r})"

class Genre(db.Model):
  '''
  Genre model Class
  '''
  __tablename__ = 'genre'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(80))

'''
  genre, n to many table
'''
genres = db.Table('genres',
  db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
  db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
  db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
)
