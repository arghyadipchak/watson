from datetime import datetime as dt
from discord.ext import commands
from utils.setup import setup_cog

class Misc(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.itime = dt.now()

  @commands.command(name="hi")
  async def hi(self, ctx: commands.Context):
    await ctx.send(f"Hi {ctx.author.mention}!")

  @commands.command(name="ping")
  async def ping(self, ctx: commands.Context):
    await ctx.send(f"Pong! My latency is {round(self.bot.latency*1000, 2)}ms")

  @commands.command(name="stime")
  async def stime(self, ctx: commands.Context):
    await ctx.send(f"Bot started at: {str(self.itime)[:-7]}")
  
  @commands.command(name="uptime", aliases=["utime"])
  async def uptime(self, ctx: commands.Context):
    upt = dt.now() - self.itime
    await ctx.send(f"Bot Uptime: {str(upt)[:-7]}")

setup = setup_cog(Misc)