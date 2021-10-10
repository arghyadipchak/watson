from json import dump, load
from requests import get, put
from yaml import safe_dump, safe_load

class Data(dict):
  def __init__(self: dict, loct: str = 'data.yml'):
    self.loct = loct
    try:
      if self.loct.startswith('http://') or self.loct.startswith('https://'):
        with get(url=loct) as resp:
          assert resp.status_code==200
          dst = resp.content
      else:
        with open(loct, 'r') as fh:
          dst = fh.read()
      if self.loct.endswith('.json'):
        data = load(dst)
      elif self.loct.endswith('.yml') or self.loct.endswith('.yaml'):
        data = safe_load(dst)
    except:
      data = {}
    super(Data, self).__init__(data)

  def save(self: dict):
    if self.loct.endswith('.json'):
      dst = dump(dict(self), indent=2)
    elif self.loct.endswith('.yml') or self.loct.endswith('.yaml'):
      dst = safe_dump(dict(self), indent=2)
    if self.loct.startswith('http://') or self.loct.startswith('https://'):
      with put(url=self.loct, data=dst) as resp:
        assert resp.status_code==200
    else:
      with open(self.loct, 'w') as fh:
        fh.write(dst)