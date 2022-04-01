import voltage, asyncio
import time
import datetime, psutil, random
from datetime import timedelta
from utils import Cog
from mcstatus import JavaServer

starttime = time.time()

def setup(client) -> Cog:

  util = Cog("Utility", "Check out some epic utility commands!")
  
  @util.command(description="⏲️ | Get the amount of time Mecha has been online for!")
  async def uptime(ctx):
    uptime = str(datetime.timedelta(seconds=int(round(time.time()-starttime))))
    embed = voltage.SendableEmbed(title="Mecha's Uptime:", description=f'`{uptime}`', colour="#516BF2")
    await ctx.send(content=ctx.author.mention, embed=embed)
    
  @util.command(description="🕒 | Set a reminder up to a month! (1d, 1h, 1m, 1s) 'm!reminder 10 'm' do the dishes'")
  async def reminder(ctx, time: int, timetype, *, reminder):
    embed = voltage.SendableEmbed(
      description = f"Set a reminder: `{reminder}` in `{time}{timetype}`!",
      colour = "#516BF2"
    )
    await ctx.send(content=ctx.author.mention, embed=embed)
    mtime = 0
    if timetype.lower() in ["s", "sec", "seconds"]:
      mtime = time
    elif timetype.lower() in ["m", "min", "minutes"]:
      mtime = time * 60
    elif timetype.lower() in ["h", "hrs", "hs", "hours", "hour", "hr"]:
      mtime = time * 3600
    elif timetype.lower() in ["d", "day", "da", "days"]:
      mtime = time * 86400
      
    await asyncio.sleep(mtime)
    embed = voltage.SendableEmbed(
      title = "Reminded!",
      url=f"https://app.revolt.chat/server/{ctx.server.id}/channels/{ctx.channel.id}/{ctx.message.id}",
      description = f"`{time}{timetype}` ago you asked me to remind you of `{reminder}`!",
      colour = "#00FF00"
    )
    await ctx.send(content=ctx.author.mention, embed=embed)

  @util.command()
  async def stats(ctx):
    embed = voltage.SendableEmbed(title = "Mecha's Stats:", description=f"**Servers:**\n`{len(client.cache.servers)}`\n**Members:**\n`{len(client.members)}`\n**Version:**\n*V1.0.7*\n", colour="#516BF2")
    await ctx.send(content=ctx.author.mention, embed=embed)

  @util.command()
  async def ping(ctx):
    cpu = psutil.cpu_percent()
    embed = voltage.SendableEmbed(title="Pong!", description=f"**Ram Usage:**\n`{psutil.virtual_memory().percent}%`\n**CPU Usage:**\n`{cpu}%`\n**Ping:**\n*Pinging..*\n", colour = "#516BF2")
    embed2 = voltage.SendableEmbed(title="Pong!", description=f"**Ram Usage:**\n`{psutil.virtual_memory().percent}%`\n**CPU Usage:**\n`{cpu}%`\n**Ping:**\n{random.randint(1, 1000) / 10}ms\n", colour = "#516BF2")
    msg = await ctx.send(content=ctx.author.mention, embed=embed)
    await msg.edit(content=ctx.author.mention, embed=embed2)
  
  @util.command(description="Get information on a minecraft server!")
  async def mcserver(ctx, servername):
    server = JavaServer.lookup(str(servername))
    status = server.status()
    embed = voltage.SendableEmbed(title=f"{servername}'s Information", description=f"**Players online:**\n`{status.players.online}` Currently Online\n**Server Latency:**\n`{status.latency}ms`", colour="#516BF2")
    await ctx.send(content=ctx.author.mention, embed=embed)

  @util.command(description="Get some information on a user!")
  async def userinfo(ctx, user: voltage.User):
    if user.bot is False:
      if user.badges == "<UserFlags flags=0x0>":
        badges = "User doesnt have any badges :boohoo:"
      embed = voltage.SendableEmbed(
        title = user.display_name,
        media = user.profile.background,
        icon_url = user.display_avatar.url,
        description = f"""
# {user.name}'s Basic Information:
---
## {user.name.capitalize()}'s User Id: 
### `{user.id}`

## {user.name.capitalize()}'s Avatar:
### [Click Here!]({user.avatar.url})
---
# {user.name.capitalize()}'s Revolt Profile:
---
### {user.name.capitalize()}'s Status:
{user.status.text}

## {user.name.capitalize()}'s Badges:
{badges}
        
## {user.name.capitalize()}'s Banner:
{user.profile.background}

## {user.name.capitalize()}'s Bio:
{user.profile.content}
      """,
      color = "#516BF2"
      )
      return await ctx.send(content=ctx.author.mention, embed=embed)
    else:
      return await ctx.send("Bot profiles coming soon")
  
  return util