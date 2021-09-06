from models.bot import WatsonBot
from os import getenv
import pytest
from utils.config import Config

def main():
  config = Config(getenv('CONFIG_LOCT', default='config.yml'))
  bot = WatsonBot(config=config)
  bot.run(config['bot']['token'])

@pytest.mark.asyncio
async def test():
  config = Config(getenv('CONFIG_LOCT', default='config.yml'))
  bot = WatsonBot(config=config)
  await bot.login(config['bot']['token'])
  await bot.close()

if __name__=='__main__':
  main()