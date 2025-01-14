import nextcord
from nextcord.ext import commands
import os

bot = commands.Bot(command_prefix="!", intents=nextcord.Intents.all())

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game("Bedwars"))
    print("\nR.A.L.P.H.\nStatus: Online\nAwaiting Prompt\n")
  
initial_extensions=[]
for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    initial_extensions.append("cogs." + filename[:-3])
if __name__=='__main__':
  for extension in initial_extensions:
    bot.load_extension(extension)

TOKEN=""
bot.run(TOKEN)
