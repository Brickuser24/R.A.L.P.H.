import requests
import nextcord
from nextcord.ext import commands

coverage_options = {
    "Normal": ["Fighting", "Psychic", "Dark"],
    "Water": ["Ice", "Steel", "Psychic"],
    "Poison": ["Bug", "Grass", "Electric"],
    "Psychic": ["Fairy", "Ghost", "Water"],
    "Fighting": ["Electric", "Ice", "Fire"],
    "Flying": ["Steel", "Dragon", "Fighting"],
    "Grass": ["Ground", "Poison", "Rock"],
    "Ground": ["Rock", "Grass", "Dark"],
    "Bug": ["Dark", "Poison", "Ground"],
    "Rock": ["Ground", "Fire", "Electric"],
    "Dark": ["Rock", "Electric", "Poison"],
    "Fairy": ["Psychic", "Water", "Grass"],
    "Steel": ["Ice", "Ground", "Ghost"],
    "Ghost": ["Poison", "Flying", "Bug"],
    "Ice": ["Water", "Fairy", "Steel"],
    "Dragon": ["Fire", "Grass", "Psychic"],
    "Electric": ["Fairy", "Grass", "Dragon"],
    "Fire": ["Dragon", "Electric", "Fighting"]
}

class pokemon_info(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pokemon(self, ctx, pokemon):
      try:
        url = "https://pokeapi.co/api/v2/pokemon/" + pokemon.lower()
        data = requests.get(url).json()
        name = data['name'].title()
        image_url = data['sprites']['front_default']
        base_stats = {}
        for stat in data["stats"]:
          base_stats[stat["stat"]["name"]] = stat["base_stat"]
        types = [type_data["type"]["name"].capitalize() for type_data in data["types"]]
        coverages = []
        for type in types:
          for coverage in coverage_options[type]:
            if coverage not in coverages:
              coverages.append(coverage)
        embed=nextcord.Embed(title=f"{name} Info", color=nextcord.Colour.blue())
        embed.set_thumbnail(url=image_url)
        embed.add_field(name="Type",value=f"{types}",inline=False)
        basestats={"Hp": base_stats['hp'],"Atk": base_stats['attack'], "Def": base_stats['defense'], "SpAtk": base_stats['special-attack'], "SpDef": base_stats['special-defense'], "Spe": base_stats['speed']}
        formatted_stats = "\n".join([f"{key}: {value}" for key, value in basestats.items()])
        embed.add_field(name="Base Stats",value=f"{formatted_stats}",inline=False)
        embed.add_field(name="Coverage Options",value=f"{coverages}",inline=False)
        await ctx.send(embed=embed)
      except:
        await ctx.send("Invalid Pokemon")

def setup(client):
  client.add_cog(pokemon_info(client))
