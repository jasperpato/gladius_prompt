import cmd
import pathlib
import re
import datetime

parent = pathlib.Path(__file__).parent

AIRPORT_CODES = [line.strip() for line in open(parent / '../../iata_codes/airport_codes.txt', 'r')]
AIRLINE_CODES = [line.strip() for line in open(parent / '../../iata_codes/airline_codes.txt', 'r')]
CABIN_TYPES = 'PFJCSY'

SHOP_RESPONSE = 'OK'
AIR_RESPONSE = 'OK'
ERROR_REPONSE = 'Error'

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
  if re.fullmatch(f'{d}{d}{d}{d}-{d}{d}-{d}{d}', date):
    today = datetime.date.today()
    date = datetime.date(int(date[:4]), int(date[5:7]), int(date[8:10]))
    if (diff := (date - today).days) > 0:
      return diff
  return False

def is_valid_shop_date(date: str):
  return (diff := is_valid_air_date(date)) and diff <= 100

def is_valid_seats(seats: str):
  try: return (i:=int(seats)) >= 1 and i <= 10
  except: return False

# ----- parsing functions -----

def parse_shop(args: list[str]):
  if len(args) >= 7 and (
    args[:2] == ['flight', 'fares'] and
    is_valid_airport(args[2]) and
    is_valid_airport(args[3]) and
    args[2] != args[3] and (
      len(args) == 7 and args[4] == 'OneWay' or
      len(args) == 8 and args[4] == 'Return' and is_valid_trip(args[5])
    ) and
    is_valid_cabin(args[-2]) and
    is_valid_shop_date(args[-1])
  ):
    return SHOP_RESPONSE
  else:
    return ERROR_REPONSE

def parse_segments(segments: list[list[str]]):
  for seg in segments:
    if (
      len(seg) != 6 or
      not is_valid_airport(seg[0]) or
      not is_valid_airport(seg[1]) or
      seg[0] == seg[1] or
      not is_valid_airline(seg[2]) or
      not is_valid_air_date(seg[3]) or
      not is_valid_cabin(seg[4]) or
      not is_valid_seats(seg[5])
    ):
      return ERROR_REPONSE
  return AIR_RESPONSE

# ----- REPL -----

class GladiusPrompt(cmd.Cmd):
    init_prompt = 'gladius> '
    prompt = init_prompt

    def __init__(self, reply=True):
      super().__init__()
      self.reply = reply
      self.last_response = ''
      self.in_air = False
      self.segments = []

    def default(self, _):
      self.last_response = ERROR_REPONSE
      if self.reply:
        print(self.last_response)

    def do_shop(self, arg: str):
      args = arg.split()
      self.last_response = parse_shop(args)
      if self.reply: print(self.last_response)
      
    def do_air(self, arg: str):
      args = arg.split()
      if args[:2] == ['book', 'req']:
        self.in_air = True
        self.segments = []
        self.__class__.prompt = '... '.rjust(len(self.__class__.init_prompt))

    def do_seg(self, arg: str):
      if self.in_air:
        args = arg.split()
        self.segments.append(args)
      elif self.reply:
        self.last_response = ERROR_REPONSE
        print(self.last_response)

    def do_EOC(self, _):
      if self.segments:
        self.last_response = parse_segments(self.segments)
        if self.reply: print(self.last_response)
        self.in_air = False
        self.__class__.prompt = self.__class__.init_prompt
      elif self.reply:
        self.last_response = ERROR_REPONSE
        print(self.last_response)

# --------------------

if __name__ == '__main__':
  g = GladiusPrompt()
  g.cmdloop()