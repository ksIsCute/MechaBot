import voltage, json, time
from time import time
import os, random
from utils import CommandsClient, CommandNotFound, NotEnoughArgs

async def get_prefix(message, client):
  with open ("prefixes.json", "r") as f:
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

"""
@bot.listen('message')
async def on_message(message):
  if message.content == "<@01FZB4GBHDVYY6KT8JH4RBX4KR>":
    with open("prefixes.json", "r") as f:
      prefixes = json.load(f)
      prefix = prefixes.get(str(message.server.id))
    return await message.channel.send(f"Pong, {message.author.mention}! My prefix for this server is `{prefix}`")
"""

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
    

@bot.listen('ready')
async def on_ready():
  for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
      try:
        bot.add_extension(f"cogs.{filename[:-3]}")
        print(f"Just loaded {filename}")
      except Exception as e:
        print(e)

@bot.command()
async def support(ctx):
  embed=voltage.SendableEmbed(title="Need Help? Found a Bug? Want to see a feature implimented? All of the above?", description="Tell us at [Our Website](https://mechabot.tk/) or join us in [Our Server](https://app.revolt.chat/invite/hqSq0yZh)!", colour="#516BF2", media="https://i.imgur.com/3DQ7a6I.jpg")
  await ctx.send(content=ctx.author.mention, embed=embed)

@bot.command()
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
      description = error,
      colour = "#516BF2",
      media = "https://i.imgur.com/T3YNsY1.png"
    )
    return await message.reply(message.author.mention, embed=embed)

bot.run(os.environ['TOKEN'])
