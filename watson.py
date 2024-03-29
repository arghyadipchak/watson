from models.bot import WatsonBot
from models.data import Data
from os import getenv

def main():
  config = Data(getenv('CONFIG_LOCT', default='config.yml'))
  data = Data(getenv('DATA_LOCT', default='data.yml'))
  bot = WatsonBot(config=config, data=data)
  bot.run(config['bot']['token'])

if __name__=='__main__':
  main()