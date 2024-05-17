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
            "accept": "*/*",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "cookie": "_ga=GA1.1.434310172.1706248472; __gads=ID=976420f80d2fde84:T=1706248472:RT=1706248472:S=ALNI_MZv-YEMQrzO8S21pJZCTJ8eM9aUxw; __gpi=UID=00000cf05c5deecc:T=1706248472:RT=1706248472:S=ALNI_Mb0dwnF9AEPJ0PPpgxTwBhxDPwIIw; _ga_LRYLYJ15WQ=GS1.1.1706248471.1.0.1706248481.0.0.0; _ga_ZXJL7HEGYW=GS1.1.1706444920.2.1.1706444985.0.0.0",
            "pragma": "no-cache",
            "referer": f"https://stats.pika-network.net/player/{user}/bedwars",
            "sec-ch-ua": "^\^Not_A",
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": "^\^Windows^^",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
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
