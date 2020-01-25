import discord
from discord.ext import commands

class nsfw:
    def __init__(self,bot):
        self.bot = bot

    @commands.check()
    async def predicate(ctx):
        return ctx.channel.is_nsfw() is not None

    @commands.commands()
    async def check(self, ctx):
        await ctx.send("ok")

def setup(bot):
    bot.add_cog(nsfw(bot))