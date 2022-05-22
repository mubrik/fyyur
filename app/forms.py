'''
 holds classes for all forms
'''
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import (
  StringField, SelectField, 
  SelectMultipleField, DateTimeField, BooleanField, IntegerField
)
from wtforms.validators import DataRequired, URL, InputRequired
from .utils import is_phone_valid, Genre, State

# state_choices = [
#   ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'),
#   ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'),
#   ('DC', 'DC'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'),
#   ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'),
#   ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'),
#   ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'),
#   ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'),
#   ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'),
#   ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'),
#   ('MS', 'MS'), ('MO', 'MO'), ('PA', 'PA'), ('RI', 'RI'),
#   ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'),
#   ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'),
#   ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY'),
# ]

# genres_choices = [
#   ('Alternative', 'Alternative'), ('Blues', 'Blues'),
#   ('Classical', 'Classical'), ('Country', 'Country'),
#   ('Electronic', 'Electronic'), ('Folk', 'Folk'),
#   ('Funk', 'Funk'), ('Hip-Hop', 'Hip-Hop'),
#   ('Heavy Metal', 'Heavy Metal'), ('Instrumental', 'Instrumental'),
#   ('Jazz', 'Jazz'), ('Musical Theatre', 'Musical Theatre'),
#   ('Pop', 'Pop'), ('Punk', 'Punk'),
#   ('R&B', 'R&B'), ('Reggae', 'Reggae'),
#   ('Rock n Roll', 'Rock n Roll'),
#   ('Soul', 'Soul'), ('Other', 'Other'),
# ]


class CustomValidatorForm(FlaskForm):
  '''
    using inheritance to hold validate function
  '''
  def validate(self, extra_validators=None):
    # super
    returned_value = FlaskForm.validate(self, extra_validators)
    if not returned_value:
      return False
    if not is_phone_valid(self.phone.data):
      self.phone.errors.append('Phone is invalid')
      return False
    if not set(self.genres.data).issubset(dict(Genre.choices()).values()):
      self.genres.errors.append('Genre is Invalid')
      return False
    if self.state.data not in dict(State.choices()).values():
      self.state.errors.append('State is Invalid')
      return False
    # implicit pass validation
    return True


# inheriting from flaskform to use validate_on_submit method
class ShowForm(FlaskForm):
  '''
    Show form class
  '''
  artist_id = IntegerField('artist_id')
  venue_id = IntegerField('venue_id')
  start_time = DateTimeField('start_time', validators=[DataRequired()], default= datetime.today())


class VenueForm(CustomValidatorForm):
  '''
    Venue form class
  '''
  name = StringField('name', validators=[DataRequired()])
  city = StringField('city', validators=[DataRequired()])
  state = SelectField('state', validators=[DataRequired()], choices=State.choices())
  address = StringField('address', validators=[DataRequired()])
  phone = StringField('phone', validators=[InputRequired()])
  genres = SelectMultipleField('genres', validators=[DataRequired()], choices=Genre.choices())
  image_link = StringField('image_link')
  facebook_link = StringField('facebook_link', validators=[URL()])
  website_link = StringField('website_link')
  seeking_talent = BooleanField( 'seeking_talent' )
  seeking_description = StringField('seeking_description')


class ArtistForm(CustomValidatorForm):
  '''
    Artist form class
  '''
  name = StringField('name', validators=[DataRequired()])
  city = StringField('city', validators=[DataRequired()])
  state = SelectField('state', validators=[DataRequired()], choices=State.choices())
  phone = StringField('phone', validators=[InputRequired()])
  image_link = StringField('image_link')
  genres = SelectMultipleField('genres', validators=[DataRequired()], choices=Genre.choices())
  facebook_link = StringField('facebook_link', validators=[URL(), DataRequired()])
  website_link = StringField('website_link', validators=[URL()])
  seeking_venue = BooleanField( 'seeking_venue' )
  seeking_description = StringField('seeking_description')


class SongForm(FlaskForm):
  '''
    Song form class
  '''
  title = StringField('title', validators=[InputRequired()])
  artist_id = IntegerField('artist_id', validators=[InputRequired()])
  album_id = IntegerField('album_id', validators=[InputRequired()])
  length = IntegerField('length')


class AlbumForm(FlaskForm):
  '''
    Album form class
  '''
  name = StringField('name', validators=[InputRequired()])
  artist_id = IntegerField('artist_id', validators=[InputRequired()])
