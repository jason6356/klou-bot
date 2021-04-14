import discord
from discord.ext import commands


class adminCog(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('We have logged in as {0.user}'.format(self.client))

    #basic kick and ban commmand
    #so when @mention the user the function can read the mention as object to the parameter which is nice
    @commands.command()
    async def kick(self, ctx, member : discord.Member, *,reason = None):
        await member.kick(reason = reason)

    #ban user
    @commands.command()
    async def ban(self, ctx, member : discord.Member, *, reason = None):
        await member.ban(reason = reason)
        await ctx.send(f'Banned {member.mention}')

    #unban user
    @commands.command()
    async def unban(self,ctx, *, member):
        banned_users = ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

        if(user.name,user.discriminator) == (member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.name}#{user.discriminator}')

    #clear chat 
    @commands.command()
    async def clear(self, ctx, amount = 5):
        await ctx.channel.purge(limit = amount)


#setup 
def setup(client):
    client.add_cog(adminCog(client))