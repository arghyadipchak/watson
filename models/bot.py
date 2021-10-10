from cogs import blacklist
from .data import Data
from discord import Activity, ActivityType, Intents
from discord.ext.commands import Bot
from discord.message import Message
from os import listdir

class WatsonBot(Bot):
  def __init__(self: Bot, config: Data, data: Data, *args, **kwargs):
    super(WatsonBot, self).__init__(command_prefix=config['bot']['prefix'], intents=Intents.all(), *args, **kwargs)
    self.config = config
    self.data = data

    for filename in listdir('./cogs'):
      if filename.endswith('.py') and filename[:-3] not in blacklist:
        self.load_extension(f'cogs.{filename[:-3]}')

  async def on_ready(self: Bot):
    print(f"Bot Running: {self.user}")
    await self.change_presence(activity=Activity(
      type=ActivityType.listening, name=f"{self.config['bot']['prefix']}help"))

  async def on_message(self: Bot, msg: Message):
    if msg.author.bot: return
    await self.process_commands(msg)

  async def on_disconnect(self: Bot):
    print("Bot Disconnected!")