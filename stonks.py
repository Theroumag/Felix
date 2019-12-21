import discord, json
from discord.ext import commands
from discord.utils import get

client = commands.Bot(command_prefix = "$")
with open("token.txt", "r") as f: token = f.read()

@client.event
async def on_ready():
    print("Felix online")
    await client.change_presence(activity=discord.Activity(name="Monitoring stocks"))
    client.help_command = commands.DefaultHelpCommand(no_category='Commands')


club_roles = {
    "Music Club": 624700825939214337,
    "Debate Club": 569659066947862531,
    "Movie Club": 569801128221605889,
    "Zoom Club": 586459065291636769,
    "Moblie Gaming Club": 587748636608167938,
    "Gaming Club": 595673819566440455,
    "Unsolved Science Discussion Club": 596060808849522718,
    "Tech Club": 614989284776345611,
    "The Children of Abraham": 622876272548118558,
    "Secular Humanist Exploration Club": 624700825939214337,
    "Mantra Club": 631587766647652413,
    "Inuentorism Club": 636024567659233310
}

club_stock_value = {
    "Music Club": 0,
    "Debate Club": 0,
    "Movie Club": 0,
    "Zoom Club": 0,
    "Moblie Gaming Club": 0,
    "Gaming Club": 0,
    "Unsolved Science Discussion Club": 0,
    "Tech Club": 0,
    "The Children of Abraham": 0,
    "Secular Humanist Exploration Club": 0,
    "Mantra Club": 0,
    "Inuentorism Club": 0
}

# Return info about stocks
@client.command()
async def update(ctx):
    for member in ctx.guild.members:
        for role in member.roles:
            for club, id_num in club_roles.items():
                if role.id == id_num:
                    club_stock_value[club] += 1

    async ctx.send(club_stock_value)
    with open('market.json', 'w') as f:
        json.dump(club_stock_value, f)

# Return info about stock fluctuations
@client.command()
async def market(ctx):
    with open("market.json") as f:
        async ctx.send(json.loads(f.read()))


client.run(token)
