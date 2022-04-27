import voltage, json, asyncio
import os, random
from voltage.ext import commands
from voltage import CommandNotFound, NotEnoughArgs, NotEnoughPerms, NotBotOwner, NotFoundException
from host import alive

async def get_prefix(message, client):
  with open("prefixes.json", "r") as f:
    prefixes = json.load(f)
  if message.server is None:
    return "m!"
  elif str(message.server.id) not in prefixes:
    with open("prefixes.json", "w") as f:
      prefixes[str(message.server.id)] = "m!"
      json.dump(prefixes, f, indent=2)
    return "m!"
  else:
    return prefixes.get(str(message.server.id), "m!")


class MyHelpCommand(commands.HelpCommand):
    async def send_help(self, ctx: commands.CommandContext):
        embed = voltage.SendableEmbed(
            title="Help",
            description=f"Use `{ctx.prefix}help <command>` to get help for any of our {len(ctx.client.commands)} commands.",
            colour="#516BF2",
            icon_url=ctx.author.display_avatar.url
        )
        text = "\n### **Other Commands**\n"
        for command in self.client.commands.values():
            if command.cog is None:
                text += f"> {command.name}\n"
        for i in self.client.cogs.values():
            text += f"\n### **{i.name}**\n{i.description}\n"
            for j in i.commands:
                text += f"\n> {j.name}"
        if embed.description:
            embed.description += text
        return await ctx.reply(f"[]({ctx.author.id})", embed=embed)


bot = commands.CommandsClient(get_prefix, help_command=MyHelpCommand)

async def status():
    for i in range(1, 10000):
        statuses = [
            f"Playing with {len(bot.cache.servers)} servers and {len(bot.members)} users!",
            f"Watching {len(bot.members)} users!",
            f"My waifu is better than yours!!! | {len(bot.cache.servers)} servers",
            f"Jan | {len(bot.cache.servers)} servers",
            f"guys my father just came back with the milk O_O - delta2571 | {len(bot.cache.servers)} servers",
            f"Revolt > shitcord | {len(bot.cache.servers)} servers",
            f"Jans Onlyfans: onlyfans.com/linustechtips | {len(bot.cache.servers)} servers",
            f"add automod instead | {len(bot.cache.servers)} servers",
            f":trol: | {len(bot.cache.servers)} servers"
        ]
        status = random.choice(statuses)
        await bot.set_status(status, voltage.PresenceType.online)
        await asyncio.sleep(5)


@bot.listen("message")
async def on_message(message):
    with open("prefixes.json", "r") as g:
        prefixes = json.load(g)
    if message.server.id not in prefixes:
        with open("prefixes.json", "w") as g:
            prefixes[message.server.id] = "m!"
            json.dump(prefixes, g, indent=2)
    with open("json/users.json", "r") as f:
        data = json.load(f)
        await bot.handle_commands(message)
    if message.author.id in data:
      await bot.handle_commands(message)
      pass
    elif message.server.id in prefixes:
      await bot.handle_commands(message)
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
    if message.content == "<@01FZB4GBHDVYY6KT8JH4RBX4KR>":
        await message.reply(
            f"Pong! My prefix for this server is `{prefix}`"
        )
        await bot.handle_commands(message)
    elif message.content.startswith(prefix) is True:
        if message.author.bot is False:
          await bot.handle_commands(message)
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
                json.dump(data, f, indent=2)
            return await bot.handle_commands(message)
    await bot.handle_commands(message)


@bot.command()
async def reload(ctx):
    if str(ctx.author.id) == "01FZB2QAPRVT8PVMF11480GRCD":
        await ctx.send("Reloading all cogs!")
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                try:
                    bot.reload_extension(f"cogs.{filename[:-3]}")
                    print(f"Just reloaded {filename}")
                    await ctx.send(f"Reloaded {filename}")
                except Exception as e:
                    print(e)
    else:
        await ctx.send("Get outta hea' you ain't my ownah'!")


@bot.listen("server_added")
async def server_added(server):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)
    with open("prefixes.json", "w") as f:
        prefixes[str(server.id)] = "m!"
        json.dump(prefixes, f, indent=2)
    channel = bot.cache.get_channel("01FZBBJJM9R6VYE0M5WJDGKMPT")
    embed = voltage.SendableEmbed(
        title="New Server alert!",
        description=f"## Just Joined a new server!\nNow at **{len(bot.servers)}** servers!",
        color="#516BF2",
    )
    await channel.send(content="[]()", embed=embed)


@bot.listen("member_join")
async def member_join(member):
    if str(member.server.id) == "01FZB38TYPX73VSWFMMJTZE8C5":
        print(f"{member} just joined!")
    else:
        return


@bot.listen("ready")
async def on_ready():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                bot.add_extension(f"cogs.{filename[:-3]}")
                print(f"Just loaded {filename}")
            except Exception as e:
                print(e)
    await status()


@bot.error("message")
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


alive()
bot.run(os.environ["TOKEN"])
