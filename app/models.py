'''
 holds models for all tables
'''
from typing import Dict, Any
from app import db

class BaseModel(db.Model):
  '''
    this is a base model class/models, includes fields all classes should have
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
  shows = db.relationship('Show', backref=db.backref('venue', lazy='joined'), lazy='joined')
  # genres = db.relationship('Genre', backref=db.backref('venues', lazy=True), lazy='subquery')

  def __init__(self, obj: Dict[str, Any], **kwargs):
    # https://docs.sqlalchemy.org/en/14/tutorial/metadata.html#other-mapped-class-details nice feature for a lazy person like me :)
    super(Venue, self).__init__(**kwargs)
    for key, value in obj.items():
      # should bleach value of some keys but not installed and not required in project?
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
  shows = db.relationship('Show', backref=db.backref('artist', lazy='joined'), lazy='joined')
  songs = db.relationship('Song', backref=db.backref('artist', lazy=True), lazy=True)
  albums = db.relationship('Album', backref=db.backref('artist', lazy=True), lazy=True)
  # genres = db.relationship('Genre', backref=db.backref('artists', lazy=True), lazy='subquery')

  def __init__(self, obj: Dict[str, Any], **kwargs):
    super(Artist, self).__init__(**kwargs)
    for key, value in obj.items():
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

  def __init__(self, obj: Dict[str, Any], **kwargs):
    super(Show, self).__init__(**kwargs)
    for key, value in obj.items():
      setattr(self, key, value)

  def __repr__(self):
    return f"Show(id={self.id!r} time={self.start_time})"

class Song(BaseModel):
  '''
  Song model Class
  '''
  __tablename__ = 'song'

  title = db.Column(db.String(120))
  length = db.Column(db.Integer)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)
  album_id = db.Column(db.Integer, db.ForeignKey('album.id'))

  def __init__(self, obj: Dict[str, Any], **kwargs):
    super(Song, self).__init__(**kwargs)
    for key, value in obj.items():
      setattr(self, key, value)

  def __repr__(self):
    return f"Song(id={self.id!r} title={self.title})"

class Album(BaseModel):
  '''
  Album model Class
  '''
  __tablename__ = 'album'

  name = db.Column(db.String(120))
  songs = db.relationship('Song', backref=db.backref('album', lazy=True), lazy=True)
  artist_id = db.Column(db.Integer, db.ForeignKey('artist.id'), nullable=False)

  def __init__(self, obj: Dict[str, Any], **kwargs):
    super(Album, self).__init__(**kwargs)
    for key, value in obj.items():
      setattr(self, key, value)

  def __repr__(self):
    return f"Album(id={self.id!r} title={self.name})"

