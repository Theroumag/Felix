import discord, json
from discord.ext import commands
from discord.utils import get

# Token
client = commands.Bot(command_prefix = "$")
with open("token.txt", "r") as f: token = f.read()

# Club : Role Name dict
with open('club_info.json', 'r') as f:
    club_roles = json.load(f)

# Club: Role Id dict
club_ids = {}
for guild in client.guilds:
    if guild.name == "stonks":
        for role in guild.roles:
            if role.name in club_roles.values():
                club_ids[role.name] = role.id

# Last Market Stats dict of Club: Value
with open("market.json", "r") as f:
    club_stock_values = json.load(f)

@client.event
async def on_ready():
    print("Stonks time")

    status = discord.Game("Monitering Stonks")
    await client.change_presence(status=discord.Status.idle, activity=status)
    
    client.help_command = commands.DefaultHelpCommand(no_category='Commands')

@client.command()
async def update(ctx):
    for role in ctx.author.roles:
        if role.permissions.administrator:
            await ctx.send("```This may take a while```")
            for member in ctx.author.guild:
                for role in member.roles:
                    for club, id_num in club_ids.items():
                        if role.id == id_num:
                            club_stock_values[club] += 1

            with open('market.json', 'w') as f:
                json.dump(club_stock_values, f)

    await ctx.send(f"```{club_stock_values}```")

@client.command()
async def fetch(ctx, club):
    if club in club_roles.keys():
        await ctx.send(f"The current market value of {club} is ``{club_stock_values[club]}``")
    else:
        await ctx.send(f"No club called {club} found. Please be careful to type the exact name of the desired club.")




client.run(token)
