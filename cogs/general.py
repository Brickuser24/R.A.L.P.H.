import nextcord
from nextcord.ext import commands

class commands_(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def commands(self, ctx):
        embed = nextcord.Embed(title="R.A.L.P.H. Commands", color=nextcord.Colour.blue(), description="")
        embed.add_field(name="!bedwars {username}", value="Player's BW stats on Pika Network", inline=False)
        embed.add_field(name="!pokemon {pokemon}", value="Info on a Pokemon", inline=False)
        embed.add_field(name="!followers", value="Brick's total followers on flickr", inline=False)
        embed.add_field(name="!socials", value="Links to Brick's socials", inline=False)
        embed.add_field(name="!pokemon_commands", value="Info on all Pokemon Commands", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(commands_(client))
