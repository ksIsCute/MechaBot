import voltage, asyncio, json
from utils import Cog

def setup(client) -> Cog:

  owner = Cog("Owner", "For the cool kids only! (used to test commands mostly)")

  @owner.command(name="eval", description="Run commands in multiple languages!")
  async def eval_fn(ctx, *, code):
    if ctx.author.id in ["01FZB2QAPRVT8PVMF11480GRCD", "01FZBQCQPT53YTAD86T28WV69X"]:
      languagespecifiers = ["python", "py", "javascript", "js", "html", "css", "php", "md", "markdown", "go", "golang", "c", "c++", "cpp", "c#", "cs", "csharp", "java", "ruby", "rb", "coffee-script", "coffeescript", "coffee", "bash", "shell", "sh", "json", "http", "pascal", "perl", "rust", "sql", "swift", "vim", "xml", "yaml"]
      loops = 0
      while code.startswith("`"):
          code = "".join(list(code)[1:])
          loops += 1
          if loops == 3:
              loops = 0
              break
      for languagespecifier in languagespecifiers:
          if code.startswith(languagespecifier):
              code = code.lstrip(languagespecifier)
      while code.endswith("`"):
          code = "".join(list(code)[0:-1])
          loops += 1
          if loops == 3:
              break
      code = "\n".join(f"    {i}" for i in code.splitlines())
      code = f"async def eval_expr():\n{code}" 
      async def send(text):
        await ctx.send(text)
      env = {
          "bot": client,
          "client": client,
          "ctx": ctx,
          "print": send,
          "_author": ctx.author,
          "_message": ctx.message,
          "_channel": ctx.channel,
          "_guild": ctx.server,
          "_me": ctx.me
      }
      env.update(globals())
      try:
          exec(code, env)
          eval_expr = env["eval_expr"]
          result = await eval_expr()
          if result:
            embed = voltage.SendableEmbed(
              title = "Code Ran with no errors!",
              description = result,
              colour = "#00FF00"
            )
            await ctx.send(content=ctx.author.mention, embed=embed)
      except Exception as e:
        embed = voltage.SendableEmbed(
          title = "Error occured!",
          description = f"```{languagespecifier}\n{e}\n```",
          colour = "#0000FF"
        )
        await ctx.send(content=ctx.author.mention, embed=embed)
    else:
      embed = voltage.SendableEmbed(title = "Whoops!", description = "You aren't an owner of this bot!", colour="#FFFF00")
      return await ctx.send(content=ctx.author.mention,embed=embed)
  
  @owner.command(description="Change the presence or status of Mecha!")
  async def status(ctx, *, status, presence=None):
    if ctx.author.id in ["01FZB2QAPRVT8PVMF11480GRCD", "01FZBQCQPT53YTAD86T28WV69X"]:
      if not presence:
        await client.set_status(status, voltage.PresenceType.online)
        return await ctx.send(f"Changed status to `{status}`")
      else:
        if presence.lower() == "online":
          await client.set_status(status, voltage.PresenceType.online)
          return await ctx.send(f"Changed status to `{status}` and a presence of `Online!`")
        elif presence.lower() == "idle":
          await client.set_status(status, voltage.PresenceType.idle)
          return await ctx.send(f"Changed status to `{status}` and a presence of `Idle`!")
        elif presence.lower() == "dnd" or "busy":
          await client.set_status(status, voltage.PresenceType.busy)
          return await ctx.send(f"Changed status to `{status}` and a presence of `Do Not Disturb`!")
    else:
      return await ctx.send("You aren't an owner of this bot!")
  @owner.command()
  async def test(ctx):
    embed = voltage.ImageEmbed(
      url = "https://i.imgur.com/2LNlDQW.jpg"
    )
    await ctx.send(content="[]()", embed=embed)
  @owner.command(description="Test our command")
  async def register(ctx):
    with open("json/users.json", "r") as f:
      data = json.load(f)
    with open("json/users.json", "w") as f:
      data[ctx.author.id] = {"username": ctx.author.name, "id": ctx.author.id, "bio": "User has no bio set!", "beta": "False", "ff": "False"}
      json.dump(data, f, indent=2)
    embed = voltage.SendableEmbed(
      description = "You're registered!"
    )
    await ctx.send(content="[]()", embed=embed)
  @owner.command(description="Use this after registering")
  async def ar(ctx):
    with open("json/users.json", "r") as f:
      data = json.load(f)
    embed = voltage.SendableEmbed(
      description = f"{data[ctx.author.id]['username']}'s profile:\n\n**Bio:**\n{data[ctx.author.id]['bio']}\n\n**User's settings:**\n\nBeta: `{data[ctx.author.id]['beta']}`\nFamily Friendly Mode: `{data[ctx.author.id]['ff']}`"
    )
    await ctx.send(content="[]()", embed=embed)
  return owner