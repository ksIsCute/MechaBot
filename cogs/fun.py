import voltage, json, requests, aiohttp, random
from utils import Cog

def setup(client) -> Cog:

  fun = Cog("Fun", "Have some fun and play around with Mechas Commands!")

  @fun.command(description="How long is your pp?", aliases=["pp", "ppsize", "getpp", "whatsmypp", "penismeter", "ppmeter"])
  async def ppmeter(ctx):
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
      "-"
    ]
    embed = voltage.SendableEmbed(title = "Your PP:", description = f"8{random.choice(ppmeter)}D", colour="#516BF2")
    await ctx.send(content=ctx.author.mention, embed=embed)
  
  @fun.command(description="Get some cute doggo pics!", aliases=["dogpic", "doggos", "dogs", "dogpics", "dogpictures", "getdog", "getdogs", "dog"])
  async def dog(ctx):
    async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/dog')
      dogjson = await request.json()
      request2 = await session.get('https://some-random-api.ml/facts/dog')
      factjson = await request2.json()
  
      embed = voltage.SendableEmbed(title="Doggo!", media=dogjson['link'], colour="#516BF2", description=factjson['fact'])
      await ctx.send(content=ctx.author.mention, embed=embed)
  
  @fun.command(description="Get some cute cat pics for your collection!", aliases=["kitties", "kitty", "cats", "catpic", "kittypic", "catpicture", "cat"])
  async def cat(ctx):
    async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/cat')
      catjson = await request.json()
      request2 = await session.get('https://some-random-api.ml/facts/cat')
      factjson = await request2.json()
  
      embed = voltage.SendableEmbed(title="Meeeooowww!", media=catjson['link'], colour="#516BF2", description=factjson['fact'])
      await ctx.send(content=ctx.author.mention, embed=embed)
  
  @fun.command(description="Get some rockin' bird pics :sunglasses:", aliases=["birb", "berd", "birbpic", "birdpic", "berdpic", "bird"])
  async def bird(ctx):
    async with aiohttp.ClientSession() as session:
      request = await session.get('https://some-random-api.ml/img/birb')
      birbjson = await request.json()
      request2 = await session.get('https://some-random-api.ml/facts/birb')
      factjson = await request2.json()
      
      embed = voltage.SendableEmbed(title="Tweet tweet!1!", media=birbjson['link'],
      colour="#516BF2", description=factjson['fact'])
      await ctx.send(content=ctx.author.mention, embed=embed)
        
  return fun