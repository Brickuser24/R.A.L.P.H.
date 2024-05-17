from nextcord.ext import commands

class socials(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def socials(self, ctx):
        await ctx.send("Brick's Socials!\nFlickr: <https://www.flickr.com/photos/191092571@N03/>\nLinktree: <https://linktr.ee/brickuser24/>")
      
def setup(client):
    client.add_cog(socials(client))
