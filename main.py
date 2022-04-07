import voltage, json, asyncio
import os, random
from utils import CommandsClient, CommandNotFound, NotEnoughArgs
from host import alive

async def get_prefix(message, client):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  if message.server is None:
    return
  elif str(message.server.id) not in prefixes:
    with open("prefixes.json", "w") as f:
      prefixes[str(message.server.id)] = "m!"
      json.dump(prefixes, f, indent=2)
  else:
    return prefixes.get(str(message.server.id), "m!")

bot = CommandsClient(get_prefix)

async def status():
  for i in range(1, 10000):
    statuses = [
      f"Playing with {len(bot.cache.servers)} servers and {len(bot.members)} users!",
      f"Watching {len(bot.members)} users!",
      f"My waifu is better than yours!!! | {len(bot.cache.servers)} servers",
      f"Jan | {len(bot.cache.servers)} servers",
      f"guys my father just came back with the milk O_O - delta2571 | {len(bot.cache.servers)} servers",
      f"Revolt > shitcord | {len(bot.cache.servers)} servers",
      f"Jans Onlyfans: onlyfans.com/linustechtips | {len(bot.cache.servers)} servers"
    ]
    status = random.choice(statuses)
    await bot.set_status(status, voltage.PresenceType.online)
    await asyncio.sleep(5)

@bot.listen('message')
async def on_message(message):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
    prefix = prefixes.get(str(message.server.id))
  if message.content == "<@01FZB4GBHDVYY6KT8JH4RBX4KR>":
    await message.channel.send(f"Pong, {message.author.mention}! My prefix for this server is `{prefix}`")
  elif message.content.startswith(prefix) is True:
    print(prefix)
    print(message.content.startswith(prefix))
    if message.author.bot is False:
      pass
    else:
      return
  await bot.handle_commands(message)


@bot.command()
async def reload(ctx):
  if str(ctx.author.id) == "01FZB2QAPRVT8PVMF11480GRCD":
    await ctx.send("Reloading all cogs!")
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        try:
          bot.reload_extension(f"cogs.{filename[:-3]}")
          print(f"Just reloaded {filename}")
          await ctx.send(f"Reloaded {filename}")
        except Exception as e:
          print(e)
  else:
    await ctx.send("Get outta hea' you ain't my ownah'!")
    

@bot.listen('server_added')
async def server_added(server):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  with open("prefixes.json", "w") as f:
    prefixes[str(server.id)] = "m!"
    json.dump(prefixes, f, indent=2)
  channel = bot.cache.get_channel("01FZBBJJM9R6VYE0M5WJDGKMPT")
  embed = voltage.SendableEmbed(title="New Server alert!", description=f"## Just Joined a new server!\nNow at **{len(bot.servers)}** servers!", color="#00FF00")
  await channel.send(content="[]()", embed=embed)

@bot.listen("member_join")
async def member_join(member):
  if str(member.server.id) == "01FZB38TYPX73VSWFMMJTZE8C5":
    for role in member.server.roles:
      if role.name.lower() == "member":
        return await member.add_roles(role)
      else:
        pass
  else:
    return

@bot.listen('ready')
async def on_ready():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      try:
        bot.add_extension(f"cogs.{filename[:-3]}")
        print(f"Just loaded {filename}")
      except Exception as e:
        print(e)
  await status()

@bot.command(description="Get some support!")
async def support(ctx):
  embed=voltage.SendableEmbed(title="Need Help? Found a Bug? Want to see a feature implimented? All of the above?", description="Tell us at [Our Website](https://mechabot.tk/) or join us in [Our Server](https://app.revolt.chat/invite/hqSq0yZh)!", colour="#516BF2", media="https://i.imgur.com/3DQ7a6I.jpg")
  await ctx.send(content=ctx.author.mention, embed=embed)

@bot.command(description="Get a users avatar!")
async def avatar(ctx, member:voltage.Member):
  embed = voltage.SendableEmbed(
    title = f"{member.display_name}'s avatar!",
    media = member.display_avatar.url,
    colour = "#516BF2"
  )
  await ctx.send(content=ctx.author.mention, embed=embed)

@bot.error('message')
async def on_message_error(error: Exception, message):
  if isinstance(error, CommandNotFound):
    errormsg = [
      "Error! Error!",
      "LOOK OUT!!! ERROR!!",
      "Whoops!",
      "Oopsie!",
      "Something went wrong!",
      "Something happened..",
      "What happened? I know!",
      "404!",
      "ERROR.. ERROR..",
      "Error Occured!",
      "An Error Occured!"
    ]
    embed=voltage.SendableEmbed(
      title = random.choice(errormsg),
      description = "That command doesnt exist!",
      colour = "#516BF2",
      media = "https://i.imgur.com/NUg5Lx7.png"
    )
    return await message.reply(message.author.mention, embed=embed)
  elif isinstance(error, NotEnoughArgs):
    errormsg = [
      "Error! Error!",
      "LOOK OUT!!! ERROR!!",
      "Whoops!",
      "Oopsie!",
      "Something went wrong!",
      "Something happened..",
      "What happened? I know!",
      "404!",
      "ERROR.. ERROR..",
      "Error Occured!",
      "An Error Occured!"
    ]
    embed=voltage.SendableEmbed(
      title = random.choice(errormsg),
      description = "YOU'RE MISSING ARGS!",
      colour = "#516BF2",
      media = "https://i.imgur.com/IqqnqmF.png"
    )
    return await message.reply(message.author.mention, embed=embed)
  else:
    errormsg = [
      "Error! Error!",
      "LOOK OUT!!! ERROR!!",
      "Whoops!",
      "Oopsie!",
      "Something went wrong!",
      "Something happened..",
      "What happened? I know!",
      "404!",
      "ERROR.. ERROR..",
      "Error Occured!",
      "An Error Occured!"
    ]
    embed=voltage.SendableEmbed(
      title = random.choice(errormsg),
      description = Exception,
      colour = "#516BF2",
      media = "https://i.imgur.com/T3YNsY1.png"
    )
    return await message.reply(message.author.mention, embed=embed)



alive()
bot.run(os.environ['TOKEN'])
