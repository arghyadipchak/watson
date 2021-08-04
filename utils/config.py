from json import load
from os import getenv
from yaml import safe_load

def get_config(loct: str = None):
  if not loct:
    loct = getenv('CONFIG_LOCT', 'config.yml')
  
  config = {}
  if loct.endswith('.json'):
    with open(loct, 'r') as fh:
      config = load(fh)
  elif loct.endswith('.yml') or loct.endswith('.yaml'):
    with  open(loct, 'r') as fh:
      config = safe_load(fh)
  elif loct.startswith('http://') or loct.startswith('https://'):
    ...
  return config