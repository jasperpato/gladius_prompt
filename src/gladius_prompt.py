'''
A parser and read–eval–print (REPL) loop for the GLADIUS command syntax described in the project spec for CITS5501 Sem 1 2023.
Responds with 'OK' on valid commands and 'Error' on invalid commands.
If an invalid line is given within the "air book req" command, the command is aborted.
'''
 # ----- intro -----

INTRO = '''
Welcome to GLADIUS parser and REPL.
Responds with 'OK' to valid commands and 'Error' to invalid commands.
Example commands:
  - shop flight fares AAA AAB OneWay C 2023-07-07
  - air book req
    seg AAA AAB AA1 2023-07-07 C 5
    EOC

Jasper Paterson 22736341
CITS5501 Project Sem 1 2023
'''

import cmd
import pathlib
import re
import datetime

parent = pathlib.Path(__file__).parent

AIRPORT_CODES = [line.strip() for line in open(parent / '../iata_codes/airport_codes.txt', 'r')]
AIRLINE_CODES = [line.strip() for line in open(parent / '../iata_codes/airline_codes.txt', 'r')]

CABIN_TYPES = 'PFJCSY'

# ----- validation functions -----

def is_valid_airport(code: str):
  return code in AIRPORT_CODES

def is_valid_airline(airline: str):
  d = '[0-9]'
  return airline[:2] in AIRLINE_CODES and re.fullmatch(f'{d}({d}?){{3}}', airline[2:])

def is_valid_trip(trip: str):
  try: return (i:=int(trip)) >= 0 and i <= 20
  except: return False

def is_valid_cabin(cabin: str):
  return cabin in CABIN_TYPES

def is_valid_air_date(date: str):
  d = '[0-9]'
  try:
    if re.fullmatch(f'{d}{d}{d}{d}-{d}{d}-{d}{d}', date):
      today = datetime.date.today()
      date = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10]))
      if (diff := (date - today).days) > 0:
        return diff
  except: pass
  return False

def is_valid_shop_date(date: str):
  return (diff := is_valid_air_date(date)) and diff <= 100

def is_valid_seats(seats: str):
  try: return (i:=int(seats)) >= 1 and i <= 10
  except: return False

# ----- parsing functions -----

def is_valid_shop(args: list):
  return (
    len(args) >= 7 and
    args[:2] == ['flight', 'fares'] and
    is_valid_airport(args[2]) and
    is_valid_airport(args[3]) and
    args[2] != args[3] and (
      len(args) == 7 and args[4] == 'OneWay' or
      len(args) == 8 and args[4] == 'Return' and is_valid_trip(args[5])
    ) and
    is_valid_cabin(args[-2]) and
    is_valid_shop_date(args[-1])
  )

def is_valid_segment(seg: list):
  return (
    len(seg) == 6 and
    is_valid_airport(seg[0]) and
    is_valid_airport(seg[1]) and
    seg[0] != seg[1] and
    is_valid_airline(seg[2]) and
    is_valid_air_date(seg[3]) and
    is_valid_cabin(seg[4]) and
    is_valid_seats(seg[5])
  )

# ----- REPL -----

class GladiusPrompt(cmd.Cmd):
    init_prompt = 'gladius> '
    prompt = init_prompt
    intro=INTRO

    SHOP_RESPONSE = 'OK'
    AIR_RESPONSE = 'OK'
    ERROR_RESPONSE = 'Error'

    def __init__(self, reply=True):
      super().__init__()
      self.reply = reply
      self.last_response = ''

      self.in_air = False
      self.has_segment = False

    def respond(self, msg):
      self.last_response = msg
      if self.reply: print(self.last_response)

    def error(self):
      self.respond(self.__class__.ERROR_RESPONSE)

    def reset(self):
      self.in_air = False
      self.has_segment = False
      self.__class__.prompt = self.__class__.init_prompt

    def default(self, _):
      self.reset()
      self.error()

    def do_shop(self, arg: str):
      if is_valid_shop(arg.split()):
        self.respond(self.__class__.SHOP_RESPONSE)
      else:
        self.error()
      
    def do_air(self, arg: str):
      if arg.split() == ['book', 'req']:
        self.in_air = True
        self.__class__.prompt = '... '.rjust(len(self.__class__.init_prompt))
        self.last_response = ''
      else:
        self.error()

    def do_seg(self, arg: str):
      if self.in_air and is_valid_segment(arg.split()):
        self.has_segment = True
      else:
        self.reset()
        self.error()

    def do_EOC(self, _):
      if self.has_segment:
        self.respond(self.__class__.AIR_RESPONSE)
      else:
        self.error()
      self.reset()

# --------------------

if __name__ == '__main__':
  g = GladiusPrompt()
  g.cmdloop()