from utils.bot import make_bot
from utils.config import get_config
import pytest

def main():
  config = get_config()
  bot = make_bot(config)
  bot.run(config['bot']['token'])

@pytest.mark.asyncio
async def test():
  config = get_config()
  bot = make_bot(config)
  await bot.login(config['bot']['token'])
  await bot.close()

if __name__=='__main__':
  main()