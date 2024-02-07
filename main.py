import voltage, json, asyncio
import os, random
from voltage.ext import commands
from voltage import CommandNotFound, NotEnoughArgs, NotEnoughPerms, NotBotOwner, NotFoundException
from host import alive

DEFAULT_PREFIX = "m!"

async def get_prefix(message, client):
    if message.server:
        try:
            with open ("prefixes.json", "r") as f:
                prefixes = json.load(f)
            return [prefixes.get(str(message.server.id), DEFAULT_PREFIX), client.user.mention+' ', client.user.mention]
        except:
            print("a")
            pass
    return [DEFAULT_PREFIX, client.user.mention+' ', client.user.mention]

class MyHelpCommand(commands.HelpCommand):
    async def send_help(self, ctx: commands.CommandContext):
        embed = voltage.SendableEmbed(
            title="Help",
            description=
            f"Use `{ctx.prefix}help <command>` to get help for any of our {len(ctx.client.commands)} commands.",
            colour="#516BF2",
            icon_url=ctx.author.display_avatar.url)
        text = ""
        for i in self.client.cogs.values():
            text += f"\n### **{i.name}**\n{i.description}\n"
            for j in i.commands:
                text += f"\n> {j.name}"
        if embed.description:
            embed.description += text
        return await ctx.reply(f"[]({ctx.author.id})", embed=embed)


client = commands.CommandsClient(get_prefix, help_command=MyHelpCommand, cache_message_limit=500)

async def status():
    for i in range(1, 10000):
        statuses = [
            f"Playing with {len(client.cache.servers)} servers and {len(client.members)} users!",
            f"Watching {len(client.cache.members)} users!",
            f"My waifu is better than yours!!! | {len(client.cache.servers)} servers",
            f"Jan | {len(client.cache.servers)} servers",
            f"guys my father just came back with the milk O_O - delta2571 | {len(client.cache.servers)} servers",
            f"Revolt > shitcord | {len(client.cache.servers)} servers",
            f"Jans Onlyfans: onlyfans.com/linustechtips | {len(client.cache.servers)} servers",
            f"add automod instead | {len(client.cache.servers)} servers",
            f":trol: | {len(client.cache.servers)} servers"
        ]
        status = random.choice(statuses)
        await client.set_status(status, presence=voltage.PresenceType.online)
        await asyncio.sleep(5)


"""@client.listen("message")
async def on_message(message):
    with open("prefixes.json", "r") as g:
        prefixes = json.load(g)
    if message.server.id not in prefixes:
        with open("prefixes.json", "w") as g:
            prefixes[message.server.id] = "m!"
            json.dump(prefixes, g, indent=2)
    with open("json/users.json", "r") as f:
        data = json.load(f)
    if message.author.id in data:
        pass
    elif message.server.id in prefixes:
        pass
    else:
        if message.author.id not in data:
            with open("json/users.json", "w") as f:
                data[message.author.id] = {
                    "username": message.author.name,
                    "id": message.author.id,
                    "bio": "User has no bio set!",
                    "beta": "False",
                    "ff": "False",
                    "notifications": [],
                }
                json.dump(data, f, indent=2)
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
        prefix = prefixes.get(str(message.server.id))
    if (message.content.find("<@01FZB4GBHDVYY6KT8JH4RBX4KR>") != -1):
        print("i got pinged")
        await message.reply(f"Pong! My prefix for this server is `{prefix}`")
    elif message.content.startswith(prefix) is True:
        if message.author.client is False:
            pass
        else:
            with open("json/users.json", "r") as f:
                data = json.load(f)
            if message.author.id in data:
                with open("json/users.json", "w") as f:
                    data[message.author.id] = {
                        "username": message.author.name,
                        "id": message.author.id,
                        "bio": "User has no bio set!",
                        "beta": "False",
                        "ff": "False",
                        "notifications": [],
                    }
                json.dump(data, f, indent=2)"""

@client.listen("message")
async def on_message(message: voltage.Message):
  if client.user.id in message.author.id:
    return
  if client.user.mention in message.content:
      await message.reply(f"hi {list(await get_prefix(message, client))[0]}")
      print("sent message")
  await client.handle_commands(message)

@client.command()
async def reload(ctx):
    result = {
      "owner": "❌",
      "util": "❌",
      "fun": "❌",
      "mod": "❌",
      "eco": "❌"
    }
    if str(ctx.author.id) == "01FZB2QAPRVT8PVMF11480GRCD":
        await ctx.send("Reloading all cogs!")
        try:
          client.add_extension("cogs.moddy")
          print("loaded mod cog")
          result['mod'] = "✔️"
        except Exception as e:
          print("errored out.. printing error in 3 seconds..")
          await asyncio.sleep(3)
          print(e)
        try:
          client.add_extension("cogs.ownah")
          print("loaded owner command cog")
          result['owner'] = "✔️"
        except Exception as e:
          print("errored out.. printing error in 3 seconds..")
          await asyncio.sleep(3)
          print(e)
        try:
          client.add_extension("cogs.funny")
          print("loaded fun stuff cog")
          result['fun'] = "✔️"
        except Exception as e:
          print("errored out while loading the fun cog.. printing error in 3 seconds..")
          await asyncio.sleep(3)
          print(e)
        try:
          client.add_extension("cogs.utils")
          print("loaded utility cog")
          result['util'] = "✔️"
        except Exception as e:
          print("errored out.. (while loading utility cog) printing error in 3 seconds..")
          await asyncio.sleep(3)
          print(e)
        try:
          client.add_extension("cogs.ecocog")
          print("loaded eco cog")
          result['eco'] = "✔️"
        except Exception as e:
          print("errored out.. printing error in 3 seconds..")
          await asyncio.sleep(3)
          print(e)
        results = f"""
> Owner Cog : {result['owner']}

> Moderation Cog : {result['mod']}

> Utilities Cog : {result['util']}

> Fun Commands Cog : {result['fun']}

> Economy Cog : {result['eco']}

*Successfully loaded* **{len(client.commands)}** *commands and* **5** *cogs!*
        """
        embed = voltage.SendableEmbed(
            title="Document Results",
            description=
            results,
            color="#516BF2",
            media = "https://steamuserimages-a.akamaihd.net/ugc/916921071030925767/E4C8401BBD64328BBDC96D8EEE0F93D2EF77BF02/"
        )
        await ctx.reply(content="[]()", embed=embed)
    else:
        await ctx.send("Get outta hea' you ain't my ownah'!")

@client.listen("server_added")
async def server_added(server):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    with open("prefixes.json", "w") as f:
        prefixes[str(server.id)] = "m!"
        json.dump(prefixes, f, indent=2)
    channel = client.cache.get_channel("01FZBBJJM9R6VYE0M5WJDGKMPT")
    embed = voltage.SendableEmbed(
        title="New Server alert!",
        description=
        f"## Just Joined a new server!\nNow at **{len(client.servers)}** servers!",
        color="#516BF2",
    )
    await channel.send(content="[]()", embed=embed)


@client.listen("member_join")
async def member_join(member):
    if str(member.server.id) == "01FZB38TYPX73VSWFMMJTZE8C5":
        print(f"{member} just joined!")
    else:
        return

@client.listen("ready")
async def on_ready():
    print("online")
    await status()



@client.error("message")
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
            "An Error Occured!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description="That command doesnt exist!",
            colour="#516BF2",
            media="https://i.imgur.com/NUg5Lx7.png",
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
            "An Error Occured!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description="YOU'RE MISSING ARGS!",
            colour="#516BF2",
            media="https://i.imgur.com/IqqnqmF.png",
        )
        return await message.reply(message.author.mention, embed=embed)
    elif isinstance(error, NotFoundException):
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
            "An Error Occured!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description=error,
            colour="#516BF2",
            media="https://i.imgur.com/T3YNsY1.png",
        )
        return await message.reply(message.author.mention, embed=embed)
    elif isinstance(error, NotEnoughPerms):
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
            "An Error Occured!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description=error,
            colour="#516BF2",
            media="https://i.imgur.com/T3YNsY1.png",
        )
        return await message.reply(message.author.mention, embed=embed)
    elif isinstance(error, NotBotOwner):
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
            "An Error Occured!",
        ]
        embed = voltage.SendableEmbed(
            title=random.choice(errormsg),
            description="You dont own me! You cant use my owner only commands!",
            colour="#516BF2",
            media="https://i.imgur.com/T3YNsY1.png",
        )
        return await message.reply(message.author.mention, embed=embed)


try:
  client.add_extension("cogs.moddy")
  print("loaded mod cog")
except Exception as e:
  print("errored out.. printing error in 3 seconds..")
  print(e)
try:
  client.add_extension("cogs.ownah")
  print("loaded owner command cog")
except Exception as e:
  print("errored out.. printing error in 3 seconds..")
  print(e)
try:
  client.add_extension("cogs.funny")
  print("loaded fun stuff cog")
except Exception as e:
  print("errored out while loading the fun cog.. printing error in 3 seconds..")
  print(e)
try:
  client.add_extension("cogs.utils")
  print("loaded utility cog")
except Exception as e:
  print("errored out.. (while loading utility cog) printing error in 3 seconds..")
  print(e)
try:
  client.add_extension("cogs.ecocog")
  print("loaded eco cog")
except Exception as e:
  print("errored out.. printing error in 3 seconds..")
  print(e)

alive()
client.run(os.environ["TOKEN"])
