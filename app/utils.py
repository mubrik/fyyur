'''
  utility function and classes etc
'''
import enum
import re
from typing import List, Dict
from flask import flash


class State(enum.Enum):
  AL = 'AL'
  AK = 'AK'
  AZ = 'AZ'
  AR = 'AR'
  CA = 'CA'
  CO = 'CO'
  CT = 'CT'
  DE = 'DE'
  DC = 'DC'
  FL = 'FL'
  GA = 'GA'
  HI = 'HI'
  ID = 'ID'
  IL = 'IL'
  IN = 'IN'
  IA = 'IA'
  KS = 'KS'
  KY = 'KY'
  LA = 'LA'
  ME = 'ME'
  MT = 'MT'
  NV = 'NV'
  NH = 'NH'
  NJ = 'NJ'
  NM = 'NM'
  NY = 'NY'
  NC = 'NC'
  ND = 'DE'
  OH = 'OH'
  OK = 'OK'
  OR = 'OR'
  MD = 'MD'
  MA = 'MA'
  MI = 'MI'
  MN = 'MN'
  MS = 'MS'
  MO = 'MO'
  PA = 'PA'
  RI = 'RI'
  SC = 'SC'
  SD = 'SD'
  TN = 'TN'
  TX = 'TX'
  UT = 'UT'
  VT = 'VT'
  VA = 'VA'
  WA = 'WA'
  WV = 'WV'
  WI = 'WI'
  WY = 'WY'
  
  @classmethod
  def choices(cls):
    # using value as names dont match 1 to 1
    return [(choice.name, choice.value) for choice in cls]


class Genre(enum.Enum):
  Alternative = 'Alternative'
  Blues = 'Blues'
  Classical = 'Classical'
  Country = 'Country'
  Electronic = 'Electronic'
  Folk = 'Folk'
  Funk = 'Funk'
  Hip_Hop = 'Hip-Hop'
  Heavy_Metal = 'Country'
  Instrumental = 'Instrumental'
  Jazz = 'Jazz'
  Musical_Theatre = 'Musical Theatre'
  Pop = 'Pop'
  Punk = 'Punk'
  R_B = 'R&B'
  Reggae = 'Reggae'
  Rock_Roll = 'Rock n Roll'
  Soul = 'Soul'
  Other = 'Other'


  @classmethod
  def choices(cls):
    # using value as names dont match 1 to 1
    return [(choice.value, choice.value) for choice in cls]


def is_phone_valid(number):
  """ Validate phone numbers like:
  1234567890 - no space
  123.456.7890 - dot separator
  123-456-7890 - dash separator
  123 456 7890 - space separator

  Patterns:
  000 = [0-9]{3}
  0000 = [0-9]{4}
  -.  = ?[-. ]

  Note: (? = optional) - Learn more: https://regex101.com/
  """
  regex = re.compile('^\(?([0-9]{3})\)?[-. ]?([0-9]{3})[-. ]?([0-9]{4})$')
  return regex.match(number)


def display_form_error(errorObj: Dict[str, List[str]]):
  '''
    function for displaying error in flash message
  '''
  for val in errorObj.values():
    flash('Error: ' + ' '.join(val), 'warning')