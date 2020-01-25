import discord
import random
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, usr: discord.User, *, reas: str="No reason provided"):
        """Kicks the specified user with the given reason if any"""

        try:
            if(not usr):
                await ctx.send("User **{}** doesn't exist")
                return

            await ctx.guild.kick(user=usr, reason="[KONA] {}: {}".format(ctx.message.author, reas))
            
        except(PermissionError):
            await ctx.send("I don't have enough permissions to perform this action.")
            return

        except(discord.Forbidden):
            await ctx.send("Insufficient permissions, only server admins can run this command.")
            return

        except(Exception) as e:
            await ctx.send("```{}```".format(e))
            return
            
        await ctx.send("Successfully kicked **{}**".format(usr.name))
    
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, usr: discord.User, *, reas: str="No reason provided"):
        """Bans the specified user with the given reason if any"""

        try:
            if(not usr):
                await ctx.send("User **{}** doesn't exist")
                return

            await ctx.guild.ban(user=usr, reason="[KONA] {}: {}".format(ctx.message.author, reas))
            
        except(PermissionError):
            await ctx.send("I don't have enough permissions to perform this action.")
            return

        except(discord.Forbidden):
            await ctx.send("Insufficient permissions, only server admins can run this command.")
            return

        except(Exception) as e:
            await ctx.send("```{}```".format(e))
            return
        await ctx.send("Successfully banned **{}**".format(usr.name))
    
    @commands.command()
    async def status(self,ctx):
        """Returns some of the bot's public stats"""
        
        await ctx.send("```\nUSERS: {0}\nGUILDS: {2}\nCURRENT VOICE CONNECTIONS: {1}\nD.PY VER: {3}```".format(len(self.bot.users), len(self.bot.voice_clients), len(self.bot.guilds), discord.__version__))

def setup(bot):
    bot.add_cog(Admin(bot))
