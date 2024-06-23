import nextcord
from nextcord.ext import commands
import requests
import random
import csv
import os
spawn=False
catch=False

def get_pokemon(id=None,shiny=""):
    pokemon_id=id.lower() if id is not None else random.randint(1, 1010)
    url = f'https://pokeapi.co/api/v2/pokemon/{pokemon_id}/'
    try:
        response = requests.get(url).json()
    except:
        return None
    name = response['name'].title()
    ivs=random.randint(0,100)
    level=random.randint(1,64)
    moves=[]
    try:
        while len(moves)<4:
          num=random.randrange(len(response['moves']))
          if response['moves'][num]['move']['name'] not in moves:
            moves.append(response['moves'][num]['move']['name'])
    except:
        pass
    pokemon_natures = ["Adamant", "Bashful", "Bold", "Brave", "Calm", "Careful", "Docile", "Gentle","Hardy", "Hasty", "Impish", "Jolly", "Lax", "Lonely", "Mild", "Modest", "Naive", "Naughty", "Quiet", "Quirky", "Rash", "Relaxed", "Sassy", "Serious", "Timid"]
    nature=random.choice(pokemon_natures)
    shinyroll=0 if shiny=="shiny" else random.randrange(0,8)
    if shinyroll==0:
        shiny_sprite_url = response['sprites']['front_shiny']
        return name, shiny_sprite_url, True, ivs, level, moves, nature
    else:
        sprite_url = response['sprites']['front_default']
        return name, sprite_url, False, ivs, level, moves, nature

class pokemon(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    @commands.command()
    async def wild(self, ctx, redeem=None, shiny=""):
        author=ctx.author
        if redeem is not None and author.id==717329440304005272:
            wildmon=get_pokemon(redeem,shiny)
        else:
            wildmon=get_pokemon()
        if wildmon is not None:
            if wildmon[2] is True:
                embed = nextcord.Embed(title=f"A wild :sparkles: {wildmon[0]} appeared!", color=nextcord.Colour.blue(), description="Use !catch to throw a ball!")
            else:
                embed = nextcord.Embed(title=f"A wild {wildmon[0]} appeared!", color=nextcord.Colour.blue(), description="Use !catch to throw a ball!")
            embed.set_thumbnail(url=wildmon[1])
            embed.set_footer(text=f"Spawned by {author.name}", icon_url=author.avatar)
            global spawn
            spawn=True
            global current_spawn
            current_spawn=wildmon
            await ctx.send(embed=embed)
        else:
            await ctx.send("Invalid Pokemon")
        
    @commands.command()
    async def catch(self, ctx):
        global spawn
        if spawn is True:
            spawn=False
            global current_spawn
            author=ctx.author
            catch=random.randint(0,4)
            if catch in [0,1,2]:
                catch=True
                if current_spawn[2] is True:
                    embed = nextcord.Embed(title=f"You caught a Level {current_spawn[4]} :sparkles: {current_spawn[0]} ({current_spawn[3]}%)!", color=nextcord.Colour.blue())
                else:
                    embed = nextcord.Embed(title=f"You caught a Level {current_spawn[4]} {current_spawn[0]} ({current_spawn[3]}%)!", color=nextcord.Colour.blue())
            else:
                catch=False
                embed = nextcord.Embed(title="Your catch attempt failed!"+'\n'+f"The wild {current_spawn[0]} ran away!", color=nextcord.Colour.blue())
            embed.set_thumbnail(url=current_spawn[1])
            embed.set_footer(text=author.name, icon_url=author.avatar)
            if catch is True:
                try:
                    with open(f"cogs/pokemon_data/{author.id}.csv", "r",newline="") as f:
                        cr=csv.reader(f)
                        box=[pokemon for pokemon in cr]
                        number=len(box)+1
                        f.close()
                except:
                    number=1
                with open(f"cogs/pokemon_data/{author.id}.csv", "a",newline="") as f:
                    cw=csv.writer(f)
                    cw.writerow([current_spawn[0],current_spawn[2],current_spawn[3],current_spawn[4],current_spawn[5],current_spawn[6],current_spawn[1], number])
                    f.close()
            current_spawn=False
            await ctx.send(embed=embed)
       
    @commands.command()
    async def box(self, ctx, page=1):
        author=ctx.author
        filepath=f"cogs/pokemon_data/{author.id}.csv"
        if os.path.exists(filepath):
            with open(f"cogs/pokemon_data/{author.id}.csv", "r",newline="") as f:
                r=csv.reader(f)
                cr=list(r)
                embed = nextcord.Embed(title=f"Your Pokemon ({len(cr)})", color=nextcord.Colour.blue())
                p=(page-1)*10
                try:
                    mons=""
                    for i in range(p,p+10):
                        mon=f"`{i+1}.` {cr[i][0]}"
                        if cr[i][1]=="True":
                            mon+=" :sparkles:"
                        mon+=f":white_small_square: Lvl.{cr[i][3]} :white_small_square: {cr[i][2]}%"
                        mons+=mon+'\n'
                    embed.add_field(name="",value=mons,inline=False)
                    embed.set_footer(text=author.name, icon_url=author.avatar)
                    await ctx.send(embed=embed)
                except:
                    embed.add_field(name="",value=mons,inline=False)
                    embed.set_footer(text=author.name, icon_url=author.avatar)
                    await ctx.send(embed=embed)
        else:
            await ctx.send("You dont have any pokemon!")

    @commands.command()
    async def info(self, ctx, id=1):
        result=False
        author=ctx.author
        filepath=f"cogs/pokemon_data/{author.id}.csv"
        if os.path.exists(filepath):
            with open(f"cogs/pokemon_data/{author.id}.csv", "r",newline="") as f:
                r=csv.reader(f)
                cr=list(r)
                for pokemon in cr:
                    if pokemon[-1]==str(id):
                        result=True
                        if pokemon[1]=="True":
                            embed=nextcord.Embed(title=f"Level {pokemon[3]} :sparkles:{pokemon[0]} ({pokemon[2]}%)", color=nextcord.Colour.blue())
                        else:
                            embed=nextcord.Embed(title=f"Level {pokemon[3]} {pokemon[0]} ({pokemon[2]}%)", color=nextcord.Colour.blue())
                        embed.set_thumbnail(url=pokemon[6])
                        embed.add_field(name="",value=f"Nature: {pokemon[5]}",inline=False)
                        moves=eval(pokemon[4])
                        try:
                            embed.add_field(name="", value="Moves:\n:white_small_square:"+moves[0].title()+"\n:white_small_square:"+moves[1].title()+"\n:white_small_square:"+moves[2].title()+"\n:white_small_square:"+moves[3].title(),inline=False)
                            
                        except:
                            embed.add_field(name="", value="Moves Unvailable",inline=False)
                        embed.set_footer(text=author.name, icon_url=author.avatar)
                        break
                if result:
                    await ctx.send(embed=embed)
                else:
                    await ctx.send("Invalid Pokemon ID")

    @commands.command()
    async def reset(self, ctx):
        author=ctx.author
        filepath=f"cogs/pokemon_data/{author.id}.csv"
        os.remove(filepath)
        await ctx.send("Your Pokemon journey was reset!")

    @commands.command()
    async def pokemon_commands(self,ctx):
        embed=nextcord.Embed(title="Pokemon Commands", color=nextcord.Colour.blue())
        embed.add_field(name="!wild", value="Spawns a random pokemon", inline=False)
        embed.add_field(name="!catch", value="Throw a ball at the active wild pokemon", inline=False)
        embed.add_field(name="!box {page}", value="View your Pokemon", inline=False)
        embed.add_field(name="!reset", value="Delete all your Pokemon", inline=False)
        embed.add_field(name="!info {id}", value="View a specific pokemon's info", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(pokemon(client))
