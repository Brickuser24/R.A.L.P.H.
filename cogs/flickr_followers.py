import requests as r
from nextcord.ext import commands

class flickr_followers(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def followers(self, ctx):
      url = "https://www.flickr.com/photos/191092571@N03/"
      response = r.get(url).text
      f=response.find('followerCount')
      followers=""
      for i in response[f+15:f+20]:
        if i.isdigit():
          followers+=i
      await ctx.send(f"Brick has {followers} followers on Flickr!")

def setup(client):
  client.add_cog(flickr_followers(client))
