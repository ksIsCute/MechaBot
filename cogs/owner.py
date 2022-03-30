import voltage, asyncio
from utils import Cog

def setup(client) -> Cog:

  owner = Cog("Owner", "For the cool kids only! (used to test commands mostly)")

  @owner.command(name="eval", description="Run commands in multiple languages!")
  async def eval_fn(ctx, *, code):
    if ctx.author.id == "01FZB2QAPRVT8PVMF11480GRCD":
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
      def send(text):
        ctx.send(text)
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
        
  return owner