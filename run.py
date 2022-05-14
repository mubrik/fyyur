import os
from app import app
import dateutil.parser
import babel

def format_datetime(value, format='medium'):
  '''
    Filter datetime callback function
  '''
  print(value)
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
