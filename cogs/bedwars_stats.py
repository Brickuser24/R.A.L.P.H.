import nextcord
from nextcord.ext import commands
import requests

class bedwars_stats(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

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
            "referer": f"https://stats.pika-network.net/player/{user}/bedwars",
        }
        stats = requests.request("GET", url, headers=headers, params=querystring).json()
        categories=["Wins","Kills","Final kills","Bow kills","Beds destroyed","Highest winstreak reached"]
        for category in categories:
          try:
            stat=stats[f"{category}"]["entries"][0]['value']
            embed.add_field(name=f"{category}: {stat}",value="",inline=False)
            flag=True
          except:
            continue
        if flag is True:
          await ctx.send(embed=embed)
        else:
          await ctx.send("No stats found for this player!")
      except:
        await ctx.send ("Invalid Username")

def setup(bot):
  bot.add_cog(bedwars_stats(bot))
