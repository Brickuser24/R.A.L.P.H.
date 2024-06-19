import nextcord
from nextcord.ext import commands
import os

client = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

@client.event
async def on_ready():
    await client.change_presence(activity=nextcord.Game("Bedwars"))
    print("\nR.A.L.P.H\nStatus: Online\nAwaiting Prompt\n")

@client.event
async def on_command(ctx):
    command_name = ctx.command.name
    user = ctx.author
    channel = ctx.channel
    with open("logs.txt", "a") as f:
      f.write(f"Command '{command_name}' was used by {user} in {channel}."+"\n")
      f.close()
  
initial_extensions=[]
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    initial_extensions.append("cogs." + filename[:-3])
if __name__=='__main__':
  for extension in initial_extensions:
    client.load_extension(extension)

TOKEN=""
client.run(TOKEN)
