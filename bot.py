def make_bot(config):
  from discord import Activity, ActivityType, Intents
  from discord.ext.commands import Bot
  import os

  intents = Intents.default()
  bot = Bot(command_prefix=config['bot']['prefix'], intents=intents)

  @bot.event
  async def on_ready():
    print(f"Bot Running: {bot.user}")
    await bot.change_presence(activity=Activity(type=ActivityType.listening, name=f"{config['bot']['prefix']}help"))

  @bot.event
  async def on_message(msg):
    if msg.author.bot: return
    await bot.process_commands(msg)

  from cogs import blacklist
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and filename[:-3] not in blacklist:
      bot.load_extension(f'cogs.{filename[:-3]}')

  return bot

def main():
  from utils.config import get_config
  config =  get_config()
  bot = make_bot(config)
  bot.run(config['bot']['token'])

if __name__=='__main__':
  main()