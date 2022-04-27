import voltage, json, requests, aiohttp, random
from voltage.ext import commands

class fun(commands.Cog):

  def __init__(self, client):
      self.client = client

      self.name = "Fun"
      self.description = "Have some fun and play around with Mechas Commands!"

  @commands.command(
      description="Give someone a pat!",
      aliases=["givepat", "patmember", "patuser", "userpat", "pat"],
  )
  async def pat(self, ctx, member: voltage.Member):
      if member.id == ctx.author.id:
          async with aiohttp.ClientSession() as session:
              img = await session.get(f"https://some-random-api.ml/animu/pat")
              imgjson = await img.json()
              return await ctx.send(
                  f"{ctx.author.name} pats.. themself? Sounds lonely.. [yikes..]({imgjson['link']})"
              )
      async with aiohttp.ClientSession() as session:
          img = await session.get(f"https://some-random-api.ml/animu/pat")
          imgjson = await img.json()
          await ctx.send(
              f"{ctx.author.name} pats {member.name} [cute!]({imgjson['link']})"
          )

  # https://some-random-api.ml/animu/pat
  @commands.command(
      description="Give someone a hug!",
      aliases=["givehug", "hugmember", "huguser", "userhug", "hug"],
  )
  async def hug(self, ctx, member: voltage.Member):
      if member.id == ctx.author.id:
          async with aiohttp.ClientSession() as session:
              img = await session.get(f"https://some-random-api.ml/animu/hug")
              imgjson = await img.json()
              return await ctx.send(
                  f"{ctx.author.name} pats.. themself? How lonely **are** you? [yikes..]({imgjson['link']})"
              )
      async with aiohttp.ClientSession() as session:
          img = await session.get(f"https://some-random-api.ml/animu/hug")
          imgjson = await img.json()
          await ctx.send(
              f"{ctx.author.name} hugged {member.name} [Cute!]({imgjson['link']})"
          )

  @commands.command(
      description="Get some memes boi (contains 2016 memes)! (May cause loss of brain cells)"
  )
  async def meme(self, ctx):
      async with aiohttp.ClientSession() as session:
          memesite = await session.get(f"https://some-random-api.ml/meme")
          meme = await memesite.json()
          embed = voltage.SendableEmbed(
              title=f"Here, have a {meme['category']} meme.",
              media=meme["image"],
              description=meme["caption"],
          )
          await ctx.send(content="[]()", embed=embed)

  @commands.command(
      description="Are you gay or no?",
      aliases=["howgay", "gay", "gayrate", "amigay", "gaypercent", "gayamount"],
  )
  async def gayrate(self, ctx, member: voltage.Member = None):
      if member is None:
          member = ctx.author
      rate = random.randint(1, 100)
      embed = voltage.SendableEmbed(
          title=f"{ctx.author.name}",
          icon_url=ctx.author.avatar.url,
          description=f"🏳️‍🌈 | {member.display_name} is `{str(rate)}%` gay!",
          color="#516BF2",
      )
      await ctx.send(content="[]()", embed=embed)

  @commands.command(name="8ball", description="Seek your fortune!")
  async def _8ball(self, ctx, *, question):
      responses = [
          "I belive not",
          "I dont think so",
          "No",
          "Maybe",
          "Ask again later",
          "Yes",
          "Affirmative",
          "I Belive So",
          "Its possible",
      ]
      embed = voltage.SendableEmbed(
          title=f"{ctx.author.name}",
          icon_url=ctx.author.avatar.url,
          description=f"""My response to `{str(question)}`...\n `{random.choice(responses)}`!""",
          color="#516BF2",
      )
      await ctx.send(content="[]()", embed=embed)

  @commands.command(
      description="How long is your pp?",
      aliases=["pp", "ppsize", "getpp", "whatsmypp", "penismeter", "ppmeter"],
  )
  async def ppmeter(self, ctx):
      ppmeter = [
          "=====",
          "==========",
          "=====================",
          "=",
          "`404 Penis Not Found`",
          "-----------",
          "---",
          "---------",
          "===",
          "=============================",
          "-",
          "`Error: pp too small`",
      ]
      embed = voltage.SendableEmbed(
          title="Your PP:",
          description=f"8{random.choice(ppmeter)}D",
          colour="#516BF2",
      )
      await ctx.send(content="[]()", embed=embed)

  @commands.command(
      description="Get some cute doggo pics!",
      aliases=[
          "dogpic",
          "doggos",
          "dogs",
          "dogpics",
          "dogpictures",
          "getdog",
          "getdogs",
          "dog",
      ],
  )
  async def dog(self, ctx):
      async with aiohttp.ClientSession() as session:
          request = await session.get("https://some-random-api.ml/img/dog")
          dogjson = await request.json()
          request2 = await session.get("https://some-random-api.ml/facts/dog")
          factjson = await request2.json()

          embed = voltage.SendableEmbed(
              title="Doggo!",
              media=dogjson["link"],
              colour="#516BF2",
              description=factjson["fact"],
          )
          await ctx.send(content="[]()", embed=embed)

  @commands.command(
      description="Get some cute cat pics for your collection!",
      aliases=["kitties", "kitty", "cats", "catpic", "kittypic", "catpicture", "cat"],
  )
  async def cat(self, ctx):
      async with aiohttp.ClientSession() as session:
          request = await session.get("https://some-random-api.ml/img/cat")
          catjson = await request.json()
          request2 = await session.get("https://some-random-api.ml/facts/cat")
          factjson = await request2.json()

          embed = voltage.SendableEmbed(
              title="Meeeooowww!",
              media=catjson["link"],
              colour="#516BF2",
              description=factjson["fact"],
          )
          await ctx.send(content="[]()", embed=embed)

  @commands.command(
      description="Get some cute fox pics!",
      aliases=["foxies", "foxs", "foxes", "foxypic", "foxpic", "foxpicture", "fox"],
  )
  async def fox(self, ctx):
      async with aiohttp.ClientSession() as session:
          request = await session.get("https://some-random-api.ml/img/fox")
          catjson = await request.json()
          request2 = await session.get("https://some-random-api.ml/facts/fox")
          factjson = await request2.json()

          embed = voltage.SendableEmbed(
              title="what sound do foxes make?!",
              media=catjson["link"],
              colour="#516BF2",
              description=factjson["fact"],
          )
          await ctx.send(content="[]()", embed=embed)

  @commands.command(
      description="Get some rockin' bird pics :sunglasses:",
      aliases=["birb", "berd", "birbpic", "birdpic", "berdpic", "bird"],
  )
  async def bird(self, ctx):
      async with aiohttp.ClientSession() as session:
          request = await session.get("https://some-random-api.ml/img/birb")
          birbjson = await request.json()
          request2 = await session.get("https://some-random-api.ml/facts/birb")
          factjson = await request2.json()

          embed = voltage.SendableEmbed(
              title="Tweet tweet!1!",
              media=birbjson["link"],
              colour="#516BF2",
              description=factjson["fact"],
          )
          await ctx.send(content="[]()", embed=embed)

  @commands.command(
      description="Get some randomly generated animal pics!",
      aliases=["animals", "animal", "animalpic", "animalz", "petpic"],
  )
  async def animal(self, ctx):
      animals = ["koala", "raccoon", "kangaroo", "panda"]
      animalp = random.choice(animals)
      if animalp == "koala":
          async with aiohttp.ClientSession() as session:
              request = await session.get("https://some-random-api.ml/img/koala")
              imgjson = await request.json()
              request2 = await session.get("https://some-random-api.ml/facts/koala")
              factjson = await request2.json()
              embed = voltage.SendableEmbed(
                  title="Koala time!",
                  media=imgjson["link"],
                  colour="#516BF2",
                  description=factjson["fact"],
              )
              return await ctx.send(content="[]()", embed=embed)
      elif animalp == "raccoon":
          async with aiohttp.ClientSession() as session:
              request = await session.get("https://some-random-api.ml/img/raccoon")
              imgjson = await request.json()
              request2 = await session.get("https://some-random-api.ml/facts/raccoon")
              factjson = await request2.json()
              embed = voltage.SendableEmbed(
                  title="Trash pandas are cool!",
                  media=imgjson["link"],
                  colour="#516BF2",
                  description=factjson["fact"],
              )
              return await ctx.send(content="[]()", embed=embed)
      elif animalp == "kangaroo":
          async with aiohttp.ClientSession() as session:
              request = await session.get("https://some-random-api.ml/img/kangaroo")
              imgjson = await request.json()
              request2 = await session.get(
                  "https://some-random-api.ml/facts/kangaroo"
              )
              factjson = await request2.json()
              embed = voltage.SendableEmbed(
                  title="australian moment",
                  media=imgjson["link"],
                  colour="#516BF2",
                  description=factjson["fact"],
              )
              return await ctx.send(content="[]()", embed=embed)
      elif animal == "panda":
          async with aiohttp.ClientSession() as session:
              request = await session.get("https://some-random-api.ml/img/panda")
              imgjson = await request.json()
              request2 = await session.get("https://some-random-api.ml/facts/panda")
              factjson = await request2.json()
              embed = voltage.SendableEmbed(
                  title="who made these cuties endangered???",
                  media=imgjson["link"],
                  colour="#516BF2",
                  description=factjson["fact"],
              )
              return await ctx.send(content="[]()", embed=embed)

def setup(client) -> commands.Cog:
  return fun(client)
