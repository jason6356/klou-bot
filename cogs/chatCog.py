import discord
from discord.ext import commands
import random

class chatCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases = ['8ball', '8b'])
    async def eightball(self, ctx, *, question):
        responses = ["It is certain.",
                "It is decidedly so.",
                "Without a doubt.",
                "Yes - definitely.",
                "You may rely on it.",
                "As I see it, yes.",
                "Most likely.",
                "Outlook good.",
                "Yes.",
                "Signs point to yes.",
                "Reply hazy, try again.",
                "Ask again later.",
                "Better not tell you now.",
                "Cannot predict now.",
                "Concentrate and ask again.",
                "Don't count on it.",
                "My reply is no.",
                "My sources say no.",
                "Outlook not so good.",
                "Very doubtful."]
        await ctx.send(f'Your Question : {question}\n: Answer: {random.choice(responses)}')
        

    #change profile pic and change name to disguise user xddddd

def setup(client):
    client.add_cog(chatCog(client))