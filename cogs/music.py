import nextcord
from nextcord.ext import commands
import os

songs_dict={1:"Not Like Us", 2:"Like That"}

class music(commands.Cog):
    def __init__(self, client):
      self.client = client

    @commands.command()
    async def join(self,ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            await ctx.send(f"Joined {channel}")
        else:
            await ctx.send("You need to be in a voice channel first")
    
    @commands.command()
    async def leave(self,ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
            await ctx.send("Disconnected from the voice channel")
        else:
            await ctx.send("I'm not in a voice channel")

    @commands.command()
    async def play(self, ctx, song_number=None):
        if song_number is None:
            await ctx.send("Missing Song ID argument")
            return
        try:
            song_name=songs_dict[int(song_number)]
        except:
            await ctx.send("Invalid Song ID")
            return
        file_path=f"cogs/songs/{song_name}.mp4"
        if not ctx.voice_client:
            await ctx.send("I need to be in a voice channel to play audio")
            return
        if not os.path.isfile(file_path):
            await ctx.send("Song could not be found")
            return
        try:
            audio_source = nextcord.FFmpegPCMAudio(file_path)
            ctx.voice_client.play(audio_source)
            await ctx.send(f"Now playing: {song_name}")

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

    @commands.command()
    async def stop(self,ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("Stopped playing the current song")
        else:
            await ctx.send("No song is currently playing")

    @commands.command()
    async def album(self, ctx, page=1):
        songs=[]
        start=(page-1)*10+1
        try:
            for song in range(start,start+10):
                songs.append([song, songs_dict[song]])
        except:
            pass
        finally:
            embed = nextcord.Embed(title=f"Album (Page {page})", color=nextcord.Colour.blue(), description="")
            for i in songs:
                embed.add_field(name="", value=f"`{i[0]}.` {i[1]}", inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    async def music_commands(self, ctx):
        embed=nextcord.Embed(title="Music Commands", color=nextcord.Colour.blue())
        embed.add_field(name="!join", value="Join a Voice Call", inline=False)
        embed.add_field(name="!leave", value="Leave a Voice Call", inline=False)
        embed.add_field(name="!play {id}", value="Play a Song with the given ID", inline=False)
        embed.add_field(name="!album {page}", value="View all available Songs", inline=False)
        embed.add_field(name="!stop", value="Stop playing the current Song", inline=False)
        await ctx.send(embed=embed)
        
def setup(client):
  client.add_cog(music(client))
