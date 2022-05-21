import os
from app import app
from datetime import datetime
import dateutil.parser
import babel
import logging
from logging import Formatter, FileHandler

def format_datetime(value, format='medium'):
  '''
    Filter datetime callback function
  '''
  # change format if instance of datetime
  if isinstance(value, datetime):
    value = value.isoformat()
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.jinja_env.filters['datetime'] = format_datetime
  app.run(host='0.0.0.0', port=port)

if not app.debug:
  file_handler = FileHandler('error.log')
  file_handler.setFormatter(
      Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
  )
  app.logger.setLevel(logging.INFO)
  file_handler.setLevel(logging.INFO)
  app.logger.addHandler(file_handler)
  app.logger.info('errors')
