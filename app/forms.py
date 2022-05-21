from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, URL, InputRequired, Regexp

# inheriting from flaskform to use validate_on_submit method
class ShowForm(FlaskForm):
  artist_id = IntegerField('artist_id')
  venue_id = IntegerField('venue_id')
  start_time = DateTimeField('start_time', validators=[DataRequired()], default= datetime.today())

class VenueForm(FlaskForm):
  name = StringField('name', validators=[DataRequired()])
  city = StringField('city', validators=[DataRequired()])
  state = SelectField(
      'state', validators=[DataRequired()],
      choices=[
          ('AL', 'AL'),
          ('AK', 'AK'),
          ('AZ', 'AZ'),
          ('AR', 'AR'),
          ('CA', 'CA'),
          ('CO', 'CO'),
          ('CT', 'CT'),
          ('DE', 'DE'),
          ('DC', 'DC'),
          ('FL', 'FL'),
          ('GA', 'GA'),
          ('HI', 'HI'),
          ('ID', 'ID'),
          ('IL', 'IL'),
          ('IN', 'IN'),
          ('IA', 'IA'),
          ('KS', 'KS'),
          ('KY', 'KY'),
          ('LA', 'LA'),
          ('ME', 'ME'),
          ('MT', 'MT'),
          ('NE', 'NE'),
          ('NV', 'NV'),
          ('NH', 'NH'),
          ('NJ', 'NJ'),
          ('NM', 'NM'),
          ('NY', 'NY'),
          ('NC', 'NC'),
          ('ND', 'ND'),
          ('OH', 'OH'),
          ('OK', 'OK'),
          ('OR', 'OR'),
          ('MD', 'MD'),
          ('MA', 'MA'),
          ('MI', 'MI'),
          ('MN', 'MN'),
          ('MS', 'MS'),
          ('MO', 'MO'),
          ('PA', 'PA'),
          ('RI', 'RI'),
          ('SC', 'SC'),
          ('SD', 'SD'),
          ('TN', 'TN'),
          ('TX', 'TX'),
          ('UT', 'UT'),
          ('VT', 'VT'),
          ('VA', 'VA'),
          ('WA', 'WA'),
          ('WV', 'WV'),
          ('WI', 'WI'),
          ('WY', 'WY'),
      ]
  )
  address = StringField('address', validators=[DataRequired()])
  phone = StringField('phone', validators=[InputRequired(), Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')])
  genres = SelectMultipleField(
    # TODO implement enum restriction
    'genres', validators=[DataRequired()],
    choices=[
      ('Alternative', 'Alternative'),
      ('Blues', 'Blues'),
      ('Classical', 'Classical'),
      ('Country', 'Country'),
      ('Electronic', 'Electronic'),
      ('Folk', 'Folk'),
      ('Funk', 'Funk'),
      ('Hip-Hop', 'Hip-Hop'),
      ('Heavy Metal', 'Heavy Metal'),
      ('Instrumental', 'Instrumental'),
      ('Jazz', 'Jazz'),
      ('Musical Theatre', 'Musical Theatre'),
      ('Pop', 'Pop'),
      ('Punk', 'Punk'),
      ('R&B', 'R&B'),
      ('Reggae', 'Reggae'),
      ('Rock n Roll', 'Rock n Roll'),
      ('Soul', 'Soul'),
      ('Other', 'Other'),
    ]
  )
  image_link = StringField('image_link')
  facebook_link = StringField('facebook_link', validators=[URL()])
  website_link = StringField('website_link')
  seeking_talent = BooleanField( 'seeking_talent' )
  seeking_description = StringField('seeking_description')

class ArtistForm(FlaskForm):
  name = StringField('name', validators=[DataRequired()])
  city = StringField('city', validators=[DataRequired()])
  state = SelectField('state', validators=[DataRequired()],
    choices=[
      ('AL', 'AL'), ('AK', 'AK'), ('AZ', 'AZ'), ('AR', 'AR'),
      ('CA', 'CA'), ('CO', 'CO'), ('CT', 'CT'), ('DE', 'DE'),
      ('DC', 'DC'), ('FL', 'FL'), ('GA', 'GA'), ('HI', 'HI'),
      ('ID', 'ID'), ('IL', 'IL'), ('IN', 'IN'), ('IA', 'IA'),
      ('KS', 'KS'), ('KY', 'KY'), ('LA', 'LA'), ('ME', 'ME'),
      ('MT', 'MT'), ('NE', 'NE'), ('NV', 'NV'), ('NH', 'NH'),
      ('NJ', 'NJ'), ('NM', 'NM'), ('NY', 'NY'), ('NC', 'NC'),
      ('ND', 'ND'), ('OH', 'OH'), ('OK', 'OK'), ('OR', 'OR'),
      ('MD', 'MD'), ('MA', 'MA'), ('MI', 'MI'), ('MN', 'MN'),
      ('MS', 'MS'), ('MO', 'MO'), ('PA', 'PA'), ('RI', 'RI'),
      ('SC', 'SC'), ('SD', 'SD'), ('TN', 'TN'), ('TX', 'TX'),
      ('UT', 'UT'), ('VT', 'VT'), ('VA', 'VA'), ('WA', 'WA'),
      ('WV', 'WV'), ('WI', 'WI'), ('WY', 'WY'),
    ]
  )
  phone = StringField(
    # TODO implement validation logic for phone 
    'phone', validators=[InputRequired(), Regexp('^[+]*[(]{0,1}[0-9]{1,4}[)]{0,1}[-\s\./0-9]*$')]
  )
  image_link = StringField('image_link')
  genres = SelectMultipleField(
    'genres', validators=[DataRequired()],
    choices=[
        ('Alternative', 'Alternative'),
        ('Blues', 'Blues'),
        ('Classical', 'Classical'),
        ('Country', 'Country'),
        ('Electronic', 'Electronic'),
        ('Folk', 'Folk'),
        ('Funk', 'Funk'),
        ('Hip-Hop', 'Hip-Hop'),
        ('Heavy Metal', 'Heavy Metal'),
        ('Instrumental', 'Instrumental'),
        ('Jazz', 'Jazz'),
        ('Musical Theatre', 'Musical Theatre'),
        ('Pop', 'Pop'),
        ('Punk', 'Punk'),
        ('R&B', 'R&B'),
        ('Reggae', 'Reggae'),
        ('Rock n Roll', 'Rock n Roll'),
        ('Soul', 'Soul'),
        ('Other', 'Other'),
    ]
  )
  facebook_link = StringField(
    # TODO implement enum restriction
    'facebook_link', validators=[URL(), DataRequired()]
  )
  website_link = StringField('website_link', validators=[URL()])
  seeking_venue = BooleanField( 'seeking_venue' )
  seeking_description = StringField('seeking_description')

class SongForm(FlaskForm):
  title = StringField('title', validators=[InputRequired()])
  artist_id = IntegerField('artist_id', validators=[InputRequired()])
  album_id = IntegerField('album_id', validators=[InputRequired()])
  length = IntegerField('length')

class AlbumForm(FlaskForm):
  name = StringField('name', validators=[InputRequired()])
  artist_id = IntegerField('artist_id', validators=[InputRequired()])