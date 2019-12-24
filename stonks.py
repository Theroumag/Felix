import discord, json, time, sqlite3
from datetime import datetime
from discord.ext import commands
from discord.utils import get

# NadekoBot.db Path & Sqlite3 connection
path = r"C:\path\to\your\nadeko\database\NadekoBot.db"
conn = sqlite3.connect(path)
c = conn.cursor()

# Token
client = commands.Bot(command_prefix = "$")
with open("token.txt", "r") as f: token = f.read()

# Club : Role Name dict
with open('club_info.json', 'r') as f:
    club_roles = json.load(f)

# Club: Role Id dict
club_ids = {}
for guild in client.guilds:
    if guild.name == "Intellectualist":
        for role in guild.roles:
            if role.name in club_roles.values():
                club_ids[role.name] = role.id

# Last Market Stats dict of Club: Value
with open("market.json", "r") as f:
    club_stock_values = json.load(f)

# Monitoring Voice Channel
monitoring = False
vc_time_joined = {}
vc_time_spent = {}
channel_to_moniter = ""

@client.event
async def on_ready():
    print("Stonks time")

    status = discord.Game("Monitering Stonks")
    await client.change_presence(status=discord.Status.idle, activity=status)
    
    client.help_command = commands.DefaultHelpCommand(no_category='Commands')

@client.event
async def on_voice_state_update(member, before, after):
    if monitoring:

        if str(before.channel) != channel_to_moniter:
            if str(after.channel) == channel_to_moniter:
               vc_time_joined[member.name] = time.time()
               print(f"{member.name} : {vc_time_joined[member.name]}")

        if str(before.channel) == channel_to_moniter:
            if str(after.channel) != channel_to_moniter:
                minutes_participating = round((time.time() - vc_time_joined[member.name])/60)
                c.execute(f"UPDATE DiscordUser SET CurrencyAmount = CurrencyAmount + {minutes_participating} WHERE Username = {member.name.split("#")[0]}")
                conn.commit()

# Be able to do $moniter channel1 $moniter channel2
@client.command()
async def monitor(ctx, channel):
    global monitoring
    global channel_to_moniter
    if channel_to_moniter == "off":
        channel_to_moniter = ""
        monitoring = False
    else:
        channel_to_moniter = channel
        monitoring = True

    channel_to_moniter = channel
    command_channel = ctx
    await ctx.send(f"People will have to connect after I have begun monitoring for their presence to be recognized")

# Untested
@client.command()
async def update(ctx):
    if (ctx.message.author.server_permissions.administrator) or (ctx.guild.owner.mention == ctx.author.mention):
        await ctx.send("This *may* take a while```")
        for member in ctx.author.guild:
            for role in member.roles:
                for club, id_num in club_ids.items():
                    if role.id == id_num:
                        club_stock_values[club] += 1

        with open('market.json', 'w') as f:
            json.dump(club_stock_values, f)

    await ctx.send(f"```{club_stock_values}```")


@client.command()
async def value(ctx, club):
    club = str(club) + " Club"
    try:
        val = club_stock_values[club]
        await ctx.send(f"The current market value of {club} is ``{val}``")
    except KeyError:
        await ctx.send(f"No club called '{club}' found.")

@client.command()
async def quit(ctx):
    if ctx.guild.owner.mention == ctx.author.mention:
        conn.close()
        await client.logout()
    else:
        await ctx.send("Only the owner of the server may use this command")


client.run(token)
