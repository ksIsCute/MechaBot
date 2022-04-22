import voltage, asyncio, random
import time, aiohttp, json, re
import datetime, psutil, random
from datetime import timedelta
from voltage.ext import commands
from mcstatus import JavaServer

starttime = time.time()
version = "1.1.2"

def setup(client) -> commands.Cog:

    util = commands.Cog("Utility", "Check out some epic utility commands!")

    @util.command(description="Get basic information on a server!")
    async def serverinfo(ctx):
        with open("json/servers.json", "r") as f:
            data = json.load(f)
        if ctx.server.id not in data:
            try:
                with open("json/servers.json", "w") as f:
                    data[ctx.server.id] = {
                        "name": ctx.server.name,
                        "members": str(len(ctx.server.members)),
                        "owner": ctx.server.owner.id,
                        "ownername": ctx.server.owner.name,
                        "banner": ctx.server.banner.url,
                        "icon": ctx.server.icon.url,
                    }
                    json.dump(data, f, indent=2)
                    embed = voltage.SendableEmbed(
                        description="Your server wasnt registered in our database, but it is now!",
                        color="#00FF00",
                    )
                    return await ctx.send(content="[]()", embed=embed)
            except Exception as e:
                return await ctx.send(e)
        elif ctx.server.owner.name != data[ctx.server.id]["ownername"]:
            with open("json/servers.json", "w") as f:
                data[ctx.server.id] = {
                    "name": ctx.server.name,
                    "members": str(len(ctx.server.members)),
                    "owner": ctx.server.owner.id,
                    "ownername": ctx.server.owner.name,
                    "banner": ctx.server.banner.url,
                    "icon": ctx.server.icon.url,
                }
                json.dump(data, f, indent=2)
                embed = voltage.SendableEmbed(
                    description="Your server wasnt registered in our database, but it is now!",
                    color="#00FF00",
                )
                return await ctx.send(content="[]()", embed=embed)
        else:
            info = data[ctx.server.id]
            embed = voltage.SendableEmbed(
                title=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url,
                description=f"**Information on {info['name']}!**\n\n**Server Owner:**\n> `{info['ownername']}`\n",
                media=info["banner"],
            )
            await ctx.send(content="[]()", embed=embed)

    @util.command(
        description="Removes some of the nsfw commands and makes Mecha family friendly PG clean"
    )
    async def ff(ctx, arg):
        if arg.lower() in ["yes", "on", "activated", "y", "online", "true"]:
            with open("json/users.json", "r") as f:
                data = json.load(f)

            with open("json/users.json", "w") as f:
                data[ctx.author.id]["ff"] = "True"
                json.dump(data, f, indent=2)
            embed = voltage.SendableEmbed(
                title=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url,
                description="Family friend mode `Activated`! | 😇",
                color="#00FF00",
            )
            await ctx.send(content="[]()", embed=embed)
        if arg.lower() in ["no", "false", "off", "deny", "removed", "n"]:
            with open("json/users.json", "r") as f:
                data = json.load(f)

            with open("json/users.json", "w") as f:
                data[ctx.author.id]["ff"] = "False"
                json.dump(data, f, indent=2)
            embed = voltage.SendableEmbed(
                title=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url,
                description="Family friend mode `Deactivated`! | 😈",
                color="#00FF00",
            )
            await ctx.send(content="[]()", embed=embed)

    @util.command(description="Get a random color!", aliases=["colour", "color"])
    async def color(ctx):
        chosen = "#%06x" % random.randint(0, 0xFFFFFF)
        print(chosen)
        await ctx.send(f"[](https://some-random-api.ml/canvas/colorviewer?hex={chosen})")
        
    @util.command(description="Get the color of a hex code as an image!", aliases=["view", "viewcolor", "gc", "getcolour", "getcolor", "viewcolour"])
    async def gc(ctx, hex):
        embed = voltage.SendableEmbed(
            title="Got it!",
            description=f"This is the color for your hex code: `{hex}`",
            color="#516BF2",
        )
        await ctx.send(
            content=f"[](https://some-random-api.ml/canvas/colorviewer?hex={hex})",
            embed=embed,
        )

    @util.command(description="⏲️ | Get the amount of time Mecha has been online for!")
    async def uptime(ctx):
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - starttime))))
        embed = voltage.SendableEmbed(
            title="Mecha's Uptime:", description=f"`{uptime}`", colour="#516BF2"
        )
        await ctx.send(content=ctx.author.mention, embed=embed)

    @util.command(
        description="🕒 | Set a reminder up to a month! (1d, 1h, 1m, 1s) 'm!reminder 10 'm' do the dishes'"
    )
    async def reminder(ctx, time: int, timetype, *, reminder):
        embed = voltage.SendableEmbed(
            description=f"Set a reminder: `{reminder}` in `{time}{timetype}`!",
            colour="#516BF2",
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
            title="Reminded!",
            url=f"https://app.revolt.chat/server/{ctx.server.id}/channels/{ctx.channel.id}/{ctx.message.id}",
            description=f"`{time}{timetype}` ago you asked me to remind you of `{reminder}`!",
            colour="#00FF00",
        )
        await ctx.send(content=ctx.author.mention, embed=embed)

    @util.command()
    async def stats(ctx):
        embed = voltage.SendableEmbed(
            title="Mecha's Stats:",
            description=f"**Servers:**\n`{len(client.cache.servers)}`\n**Members:**\n`{len(client.members)}`\n**Version:**\n*{version}*\n",
            colour="#516BF2",
        )
        await ctx.send(content=ctx.author.mention, embed=embed)

    @util.command()
    async def ping(ctx):
        cpu = psutil.cpu_percent()
        embed = voltage.SendableEmbed(
            title="Pong!",
            description=f"**Ram Usage:**\n`{psutil.virtual_memory().percent}%`\n**CPU Usage:**\n`{cpu}%`\n**Ping:**\n*Pinging..*\n",
            colour="#516BF2",
        )
        embed2 = voltage.SendableEmbed(
            title="Pong!",
            description=f"**Ram Usage:**\n`{psutil.virtual_memory().percent}%`\n**CPU Usage:**\n`{cpu}%`\n**Ping:**\n{random.randint(1, 1000) / 10}ms\n",
            colour="#516BF2",
        )
        msg = await ctx.send(content=ctx.author.mention, embed=embed)
        await msg.edit(content=ctx.author.mention, embed=embed2)

    @util.command(description="Get information on a minecraft server!")
    async def mcserver(ctx, servername):
        server = JavaServer.lookup(str(servername))
        status = server.status()
        embed = voltage.SendableEmbed(
            title=f"{servername}'s Information",
            description=f"**Players online:**\n`{status.players.online}` Currently Online\n**Server Latency:**\n`{status.latency}ms`",
            colour="#516BF2",
        )
        await ctx.send(content=ctx.author.mention, embed=embed)

    @util.command(description="Get some information on a user!")
    async def userinfo(ctx, user: voltage.User):
        if user.bot is False:
            embed = voltage.SendableEmbed(
                title=user.display_name,
                media=user.profile.background,
                icon_url=user.display_avatar.url,
                description=f"""
# {user.name}'s Basic Information:
---
`{user.name.capitalize()}'s User Id:`
> {user.id}

`{user.name.capitalize()}'s Avatar:`
> [Click Here!]({user.avatar.url})
---
# {user.name.capitalize()}'s Revolt Profile:
---
`{user.name.capitalize()}'s Status:`
> {user.status.text}

`{user.name.capitalize()}'s Badges:`
> {user.badges}
        
`{user.name.capitalize()}'s Banner:`
> {user.profile.background}

`{user.name.capitalize()}'s Bio:`
> {user.profile.content}
      """,
                color="#516BF2",
            )
            return await ctx.send(content=ctx.author.mention, embed=embed)
        else:
            return await ctx.send("Bot profiles coming soon")

    @util.command(
        aliases=["setbio", "sb", "bio", "changebio", "createbio", "cb", "sbio"]
    )
    async def bio(ctx, *, bio: str):
        if len(bio) > 250:
            return await ctx.send(
                "Your bio is too looooooooooooooooooooooooooong! Make sure its under 250 characters!"
            )
        retur = re.sub("'", "", bio)
        with open("json/users.json", "r") as f:
            bios = json.load(f)
        with open("prefixes.json", "r") as f:
            prefix = json.load(f)
        with open("json/users.json", "w") as f:
            bios[str(ctx.author.id)]["bio"] = str(retur)
            json.dump(bios, f, indent=2)
        await ctx.send(
            f"Set your bio! Check it using `{prefix.get(str(ctx.server.id))}profile`!"
        )

    @util.command(description="Check out a users profile or yours!")
    async def profile(ctx, user: voltage.User = None):
        if user is None:
            user = ctx.author
        with open("json/users.json", "r") as f:
            info = json.load(f)
        with open("prefixes.json", "r") as f:
            prefix = json.load(f)
        if user.id not in info:
            return await ctx.send(
                f"This user does NOT have a profile! Get them to create a profile using `{prefix.get(ctx.server.id)}register`!"
            )
        userbio = info[user.id]["bio"]
        if userbio == "User has no bio set!":
            with open("prefixes.json", "r") as f:
                prefix = json.load(f)
            userbio = f"This user does not have a bio set! Ask them to set a bio using `{prefix.get(str(ctx.server.id))}bio`!"
        embed = voltage.SendableEmbed(
            title=user.display_name,
            icon_url=user.display_avatar.url,
            description=f"**{user.display_name}'s bio:**\n> {str(userbio)}\n\n\n**Is {user.display_name} a beta tester?:**\n> `{info[user.id]['beta']}`\n\n\n **Does {user.display_name} have family friendly mode on?:**\n> `{info[user.id]['ff']}`\n",
            color="#516BF2",
        )
        if userbio == "User has no bio set!":
            with open("prefixes.json", "r") as f:
                prefix = json.load(f)
            return await ctx.send(
                f"{user.display_name}'s bio is unset! Tell them to set their bio using `{prefix.get(ctx.server.id)}bio`!"
            )
        await ctx.send(content="[]()", embed=embed)
        # await ctx.send(content="Ok. Here!", embed=embed)

    @util.command(description="Want to test commands and get a cool badge?")
    async def beta(ctx, arg):
        if arg.lower() in ["true", "yeah", "yes", "on", "enabled", "online"]:
            with open("json/users.json", "r") as f:
                beta = json.load(f)
            with open("json/users.json", "w") as f:
                beta[str(ctx.author.id)]["beta"] = "True"
                json.dump(beta, f, indent=2)

            embed = voltage.SendableEmbed(
                title=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url,
                description=f"Welcome to the beta club, {ctx.author.display_name}!\nWe'll send you some updates [here]() when commands need some testing!",
                color="#516BF2",
            )
        elif arg.lower() in ["no", "false", "nah", "off", "disabled", "offline"]:
            with open("json/users.json", "r") as f:
                beta = json.load(f)
            with open("json/users.json", "w") as f:
                beta[str(ctx.author.id)]["beta"] = "False"
                json.dump(beta, f, indent=2)

            embed = voltage.SendableEmbed(
                title=ctx.author.display_name,
                icon_url=ctx.author.display_avatar.url,
                description=f"Say goodbye to the beta club, {ctx.author.display_name}!\nWe'll miss you! (If you change your mind, you can always come back!)",
                color="#516BF2",
            )
        else:
            return await ctx.send("You must turn `on` or `off` the beta feature!")
        await ctx.send(content="[]()", embed=embed)

    @util.command(description="Beta testers only!")
    async def testing(ctx):
        with open("json/users.json", "r") as f:
            beta = json.load(f)
        if beta[ctx.author.id]["beta"] == "True":
            return await ctx.send("Check back soon!")
        else:
            return await ctx.send(
                "This command is for **beta testers** only! Use the `beta` command to register and come back!"
            )

    @util.command(description="Check your notifications", aliases=["inbox", "notifications", "mynotifs", "notifs", "myinbox"])
    async def inbox(ctx):
        with open("json/users.json", "r") as f:
            data = json.load(f)
        notificationlist = []
        for notification in data[ctx.author.id]["notifications"]:
            notificationlist.append(notification)
        if len(data[ctx.author.id]["notifications"]) == 0:
            embed = voltage.SendableEmbed(
                title=f"Your inbox: (0)",
                icon_url=ctx.author.display_avatar.url,
                description="You have no new notifications..\n:(",
                color="#00FF00",
            )
            await ctx.send(content="[]()", embed=embed)
        else:
            embed = voltage.SendableEmbed(
                title=f"Your inbox: ({len(data[ctx.author.id]['notifications'])})",
                icon_url=ctx.author.display_avatar.url,
                description="\n".join(notificationlist),
                color="#00FF00",
            )
            await ctx.send(content="[]()", embed=embed)
        with open("json/users.json", "r") as f:
            data = json.load(f)
        with open("json/users.json", "w") as f:
            for i in range(0, len(data[ctx.author.id]["notifications"])):
                data[ctx.author.id]["notifications"].pop(0)
                notificationlist.pop(0)
            json.dump(data, f, indent=2)
    
    return util
