# if ctx.author.permissions.kick_members:

import voltage, asyncio
import time, json
import datetime
from datetime import timedelta
from utils import Cog, CommandContext


def setup(client) -> Cog:

  mod = Cog("Moderation", "Got moderation?")
  
  @mod.command(description="BEGONE MESSAGES!")
  async def purge(ctx, amount: int) -> None:
    if not ctx.author.channel_permissions.manage_messages:
      return await ctx.send("You don't have permission to purge! Ask an administrator to give you the `manage_messages` permission.")
    starttime = time.time()
    await ctx.channel.purge(amount)
    embed = voltage.SendableEmbed(description=f"# Purged!\nPurged {amount} messages in {round(time.time() - starttime, 2)}s!", color="#00FF00")
    await ctx.send(content=ctx.author.mention, embed=embed)
      
  @mod.command(description="Set a custom prefix for this server!")
  async def sp(ctx, prefix):
    if ctx.author.permissions.manage_server:
      with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
      with open("prefixes.json", "w") as f:
        prefixes[str(ctx.server.id)] = prefix
        json.dump(prefixes, f, indent=2)
        embed=voltage.SendableEmbed(title="New Prefix!", description=f"Set this servers prefix to `{prefix}`!", colour="#516BF2")
      return await ctx.send(content=ctx.author.mention, embed=embed)
      
  @mod.command(description="Ban a user from your server!")
  async def ban(ctx, member: voltage.Member):
    if ctx.author.permissions.ban_members is False:
      return await ctx.send("You don't have the required permission `ban_members` that is required for this command!")
    if ctx.author.roles[0] > member.roles[0]:
      return await ctx.send("That user is above your top role! I cannot ban them!")
    if member.roles[0] < client.roles[0]:
      return await ctx.send("I couldnt ban the member because I do not have a high enough role to do this!")
    if ctx.author.permissions.ban_members:
      return await ctx.send(f"Attempting to ban {member.mention}!")
    if member.id == ctx.author.id:
      return await ctx.send("You can't ban yourself!")
    if member.id == "01FZB4GBHDVYY6KT8JH4RBX4KR":
      return await ctx.send("You want to ban me?! How dare you :boohoo:")
    if member.permissions.ban_members:
      return await ctx.send("This user is an administrator! I cannot ban them! Please remove their administrative permissions before continuing.")
    try:
      await member.ban()
      embed = voltage.SendableEmbed(title="Done!", description=f"Just Banned {member}!", colour="#516BF2")
      await ctx.send(content=ctx.author.mention, embed=embed)
    except Exception as e:
      await ctx.send(f"I was unable to ban {member}!\n```\n{e}\n```")
  
  return mod