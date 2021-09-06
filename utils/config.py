from models.data import Data

class Config(Data):
  def __init__(self: Data, loct: str = None):
    super(Config, self).__init__(loct)