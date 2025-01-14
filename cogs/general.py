import nextcord
from nextcord.ext import commands

class commands_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def commands(self, ctx):
        embed = nextcord.Embed(title="R.A.L.P.H. Commands", color=nextcord.Colour.blue(), description="")
        embed.add_field(name="!bedwars {username}", value="View a player's BW stats on Pika Network", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(commands_(bot))
