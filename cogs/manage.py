from discord import Embed, Member
from discord.channel import TextChannel
from discord.ext import commands
from discord.file import File
from discord.message import Message
from io import BytesIO
import json
from typing import Union
from utils.setup import setup_cog

class Manage(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name="clean", aliases=["purge"], invoke_without_command=True)
  async def clean(self, ctx: commands.Context, lim: int = 1, *args: Union[Member, TextChannel]):
    channels = [arg for arg in args if isinstance(arg, TextChannel)]
    if not channels: channels.append(ctx.channel)
    members = [arg for arg in args if isinstance(arg, Member)]
    await ctx.message.delete()

    embed = Embed(title="Cleaner", description="Cleaning Shit!", color=0x27AC30)
    embed.add_field(name="Messages Transversed", value=lim, inline=False)
    if members:
      req = lambda msg: msg.author in members
    else: 
      req = lambda msg: True
    for channel in channels:
      deleted = await channel.purge(limit=lim, check=req)
      members = list(set([str(msg.author) for msg in deleted]))
      embed.add_field(name="Channel", value=str(channel))
      embed.add_field(name="Deleted", value=len(deleted))
      embed.add_field(name="Authors", value='\n'.join(members))
      
    await ctx.send(embed=embed)

  @clean.command(name="nolog")
  async def nolog(self, ctx: commands.Context, lim: int = 1, *args: Union[Member, TextChannel]):
    channels = [arg for arg in args if isinstance(arg, TextChannel)]
    if not channels: channels.append(ctx.channel)
    members = [arg for arg in args if isinstance(arg, Member)]
    await ctx.message.delete()
    
    if members:
      req = lambda msg: msg.author in members
    else: 
      req = lambda msg: True
    for channel in channels:
      deleted = await channel.purge(limit=lim, check=req)
      members = list(set([str(msg.author) for msg in deleted]))

  @commands.group(name="embed", invoke_without_command=True)
  async def embed(self, ctx: commands.Context):
    await ctx.send("!embed has the following subcommands\n"\
      + "```!embed get <message(s)>\n!embed send <channel(s)> [attach embed jsons]```")
  
  @embed.command(name="send")
  async def send(self, ctx: commands.Context, *channels: TextChannel):
    try:
      for atmt in ctx.message.attachments:
        edict = json.loads(await atmt.read())
        embed = Embed.from_dict(edict)
        for channel in channels:
          await channel.send(embed=embed)
    except:
      await ctx.send("Error in sending Embed!")
  
  @embed.command(name="get")
  async def get(self, ctx: commands.Context, *messages: Message):
    try:
      files = []
      for message in messages:
        for embed in message.embeds:
          edict = embed.to_dict()
          fb = BytesIO(bytes(json.dumps(edict, indent=2), 'utf-8'))
          files.append(File(fb, filename=f"{edict.get('title', 'embed')}.json"))
      await ctx.send(files=files)
    except:
      await ctx.send("Error in getting Embed!")

setup = setup_cog(Manage)