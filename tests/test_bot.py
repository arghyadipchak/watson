from models.bot import WatsonBot
from models.data import Data
from os import getenv
import pytest

@pytest.mark.asyncio
async def test_bot():
  config = Data(getenv('CONFIG_LOCT', default='config.yml'))
  data = Data(getenv('DATA_LOCT', default='data.yml'))
  bot = WatsonBot(config=config, data=data)
  await bot.login(config['bot']['token'])
  await bot.close()