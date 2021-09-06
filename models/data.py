from aiohttp import ClientSession
from asyncio import get_event_loop
from io import BytesIO
from json import dump, load
from yaml import safe_dump, safe_load

async def async_get(url: str) -> BytesIO:
  async with ClientSession() as session:
    async with session.get(url=url) as resp:
      return BytesIO(await resp.read())

async def async_put(url: str, dst: str = ''):
  async with ClientSession() as session:
    async with session.put(url=url, data=dst) as resp:
      assert resp.status==200

class Data(dict):
  def __init__(self: dict, loct: str = 'data.yml'):
    self.loct = loct
    try:
      if self.loct.startswith('http://') or self.loct.startswith('https://'):
        fh = get_event_loop().run_until_complete(async_get(self.loct))
      else:
        fh = open(loct, 'r')
      if self.loct.endswith('.json'):
        data = load(fh)
      elif self.loct.endswith('.yml') or self.loct.endswith('.yaml'):
        data = safe_load(fh)
      fh.close()
    except:
      data = {}
    super(Data, self).__init__(data)

  def save(self: dict):
    if self.loct.endswith('.json'):
      dst = dump(dict(self), indent=2)
    elif self.loct.endswith('.yml') or self.loct.endswith('.yaml'):
      dst = safe_dump(dict(self), indent=2)
    if self.loct.startswith('http://') or self.loct.startswith('https://'):
      get_event_loop().run_until_complete(async_put(self.loct, dst))
    else:
      with open(self.loct, 'w') as fh:
        fh.write(dst)