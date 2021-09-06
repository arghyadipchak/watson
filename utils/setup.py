from discord.ext.commands import Cog
from models.bot import WatsonBot

def setup_cog(cog: Cog):
  def setup(bot: WatsonBot):
    bot.add_cog(cog(bot))
  return setup