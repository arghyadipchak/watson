from .config import get_config
config = get_config()

def setup_wconf(cog):
  def setup(bot):
    bot.add_cog(cog(bot, config))
  return setup

def setup_noconf(cog):
  def setup(bot):
    bot.add_cog(cog(bot))
  return setup