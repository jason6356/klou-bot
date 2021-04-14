import discord
import os
from discord.ext import commands

client = commands.Bot(command_prefix='$')

@client.command()
async def ping(ctx):
     await ctx.send(f'Pong! In {round(client.latency * 1000)}ms')
#loading the cog/extension
@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')

#unloading
@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')

#loading when the programs starts

for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

client.run('ODMwNDQ3OTAxOTA1OTExODI5.YHG04A._NzmnX4H7oISEjUBqflNBgjtYw8')
