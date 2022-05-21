from typing import List, Dict
from flask import flash

def display_form_error(errorObj: Dict[str, List[str]]):
  '''
    function for displaying error in flash message
  '''
  for val in errorObj.values():
    flash('Error: ' + ' '.join(val), 'warning')