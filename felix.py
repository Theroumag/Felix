import discord
from discord.ext import commands
from discord.utils import get

linkRegrex = re.compile(r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")

client = commands.Bot(command_prefix = "?")
with open("token.txt", "r") as f: token = f.read()

@client.event
async def on_ready():
    print("Felix")
    await client.change_presence(activity=discord.Activity(name="Monitoring stocks"))
    client.help_command = commands.DefaultHelpCommand(no_category='Commands')


@client.command()
async def info(ctx):
    # Return info about stocks

@client.command(aliases=["purge", "c", "p"])

client.run(token)