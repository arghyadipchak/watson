from collections import defaultdict
from discord.embeds import Embed
from discord.ext import commands
from oci.config import validate_config
from oci.core import ComputeClient, VirtualNetworkClient
from oci.core.models import Instance
from tabulate import tabulate
from typing import List
from utils.setup import setup_wconf

class OCI(commands.Cog):
  def __init__(self, bot, config: dict):
    self.bot = bot
    oci_config = config['oci']
    kc = oci_config['key_content']
    oci_config['key_content'] = f"{kc[:31]}\n{kc[31:-29].replace(' ','')}\n{kc[-29:]}"
    validate_config(oci_config)
    self.compartment_id = oci_config['tenancy']
    self.cc = ComputeClient(oci_config)
    self.vnc = VirtualNetworkClient(oci_config)

  def list_instances(self) -> List[Instance]:
    resp = self.cc.list_instances(self.compartment_id)
    if resp.status==200: return resp.data
    return []

  @commands.group(name="instance", aliases=["inst"], invoke_without_command=True)
  async def instance(self, ctx: commands.Context):
    await ctx.send("!instance has the following subcommands\n"\
      + "```!instance list\n!instnace start <name/id(s)>\n!instnace stop <name/id(s)>\n"\
      + "!instance reset <name/id(s)>\n!instnace terminate <name/id(s)>```")

  @instance.command(name="list")
  async def instance_list(self, ctx: commands.Context):
    instances = self.list_instances()
    if not instances:
      await ctx.send("Unable to fetch Instances!")
      return

    ipdc = defaultdict(lambda: "")
    resp = self.cc.list_vnic_attachments(self.compartment_id)
    if resp.status==200:
      for vnat in resp.data:
        resp = self.vnc.get_vnic(vnat.vnic_id)
        if resp.status==200:
          ipdc[vnat.instance_id] = resp.data.public_ip

    headers = ["Instance ID", "Name", "State", "Shape", "IPv4"]
    table = []
    for inst in instances:
      table.append([inst.id[-10:], inst.display_name, inst.lifecycle_state.title(), inst.shape[12:], ipdc[inst.id]])
    
    await ctx.send(f"""```{tabulate(table, headers=headers)}```""")

  @instance.command(name="start")
  async def instance_start(self, ctx: commands.Context, *args: str):
    instances = self.list_instances()
    if not instances:
      await ctx.send("Unable to fetch Instances!")
      return

    # embed = Embed.from_dict({
    #   'title': "OCI Remote",
    #   'description': "List of OCI Instances!",
    #   'color': int(0x27AC30),
    #   'fields': [dict(zip(('name', 'value', 'inline'), field)) for field in [
    #     ("Instance ID", '\n'.join([inst.id[-10:] for inst in instances]), True),
    #     ("Name", '\n'.join([inst.display_name for inst in instances]), True),
    #     # ("Public IP", '\n'.join([inst.public_ip_address for inst in instances]), True),
    #     ("State", '\n'.join([inst.lifecycle_state.title() for inst in instances]), True),
    #     ("Shape", '\n'.join([inst.shape for inst in instances]), True),
    #   ]]
    # })
    # await ctx.send(embed=embed)

setup = setup_wconf(OCI)