from typing import Dict, Any
from app import db

class BaseModel(db.Model):
  '''
    this is a base model class, includes fields all classes should have
    id, created and modified
  '''
  __abstract__  = True

  id = db.Column(db.Integer, primary_key=True)
  date_created = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
  date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp(), nullable=False
  )

class Venue(BaseModel):
  '''
  Venue model Class
  '''
  __tablename__ = 'venue'

  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  address = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  seeking_talent = db.Column(db.Boolean, default=False, nullable=False)
  seeking_description = db.Column(db.String(500))
  genres = db.Column(db.PickleType, default=[], nullable=False)
  shows = db.relationship('Show', backref=db.backref('venue', lazy=True), lazy=True)
  # genres = db.relationship('Genre', backref=db.backref('venues', lazy=True), lazy='subquery')

  def __init__(self, dict: Dict[str, Any], **kwargs):
    # https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#other-mapped-class-details nice feature for a lazy person like me :)
    # should bleach value of some keys
    super(Venue, self).__init__(**kwargs)
    for key, value in dict.items():
      setattr(self, key, value)

  def __repr__(self):
    return f"Venue(id={self.id!r}, name={self.name!r})"

class Artist(BaseModel):
  '''
    Artist model Class
  '''
  __tablename__ = 'artist'

  name = db.Column(db.String)
  city = db.Column(db.String(120))
  state = db.Column(db.String(120))
  phone = db.Column(db.String(120))
  image_link = db.Column(db.String(500))
  facebook_link = db.Column(db.String(120))
  website_link = db.Column(db.String(120))
  seeking_venue = db.Column(db.Boolean, default=False, nullable=False)
  seeking_description = db.Column(db.String(500))
  genres = db.Column(db.PickleType, default=[], nullable=False)
  shows = db.relationship('Show', backref=db.backref('artist', lazy=True), lazy=True)
  # genres = db.relationship('Genre', backref=db.backref('artists', lazy=True), lazy='subquery')

  def __init__(self, dict: Dict[str, Any], **kwargs):
    super(Artist, self).__init__(**kwargs)
    for key, value in dict.items():
      setattr(self, key, value)

  def __repr__(self):
    return f"Artist(id={self.id!r}, name={self.name!r}), genres={self.genres}"

class Show(BaseModel):
  '''
  Show model Class
  '''
  __tablename__ = 'show'

  start_time = db.Column(db.DateTime, nullable=False)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  venue_id = db.Column(db.Integer, db.ForeignKey('venue.id'), nullable=False)

  def __init__(self, dict: Dict[str, Any], **kwargs):
    super(Show, self).__init__(**kwargs)
    for key, value in dict.items():
      setattr(self, key, value)

  def __repr__(self):
    return f"Show(id={self.id!r} time={self.start_time})"

# no template to create, easier to make a pickled Object
# class Genre(db.Model):
#   '''
#   Genre model Class
#   '''
#   __tablename__ = 'genre'

#   id = db.Column(db.Integer, primary_key=True)
#   name = db.Column(db.String(80))

# '''
#   genre, n to many table
# '''
# genres = db.Table('genres',
#   db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'), primary_key=True),
#   db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True),
#   db.Column('venue_id', db.Integer, db.ForeignKey('venue.id'), primary_key=True)
# )
