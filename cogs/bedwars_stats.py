import nextcord
from nextcord.ext import commands
import requests

class bedwars_stats(commands.Cog):
  def __init__(self, client):
      self.client = client

  @commands.command()
  async def bedwars(self, ctx, user=None):
    if user is None:
      await ctx.send("Missing Username argument (Proper usage is !bedwars username)")
    else:
      try:
        flag=False
        embed = nextcord.Embed(title=f"{user}'s Bedwars Stats", color=nextcord.Colour.blue())
        url = f"https://stats.pika-network.net/api/profile/{user}/leaderboard"
        querystring = {"type":"bedwars","interval":"total","mode":"ALL_MODES"}
        headers = {
            "authority": "stats.pika-network.net",
            "referer": f"https://stats.pika-network.net/player/{user}/bedwars"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        stats=response.json()
        categories=["Wins","Kills","Final kills","Bow kills","Beds destroyed","Highest winstreak reached"]
        for i in categories:
          try:
            stat=stats[f"{i}"]["entries"][0]['value']
            embed.add_field(name=f"{i}: {stat}",value="",inline=False)
            flag=True
          except:
            continue
        if flag is True:
          await ctx.send(embed=embed)
        else:
          await ctx.send("No stats found for this player!")
      except:
        await ctx.send ("Invalid Username")

def setup(client):
  client.add_cog(bedwars_stats(client))
