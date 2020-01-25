import discord
from discord.ext import commands
import dbinteraction

class ServerManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    @commands.has_permissions(administrator=True)
    async def autorole(self, ctx):
        print(ctx.invoked_subcommand)
        exists = dbinteraction.dbexec("SELECT role from serverdata WHERE server_id = ?", (ctx.guild.id,))
        em = None
        if (exists == None):
            em = discord.Embed(title="Autorole is disabled for this guild.", color=discord.Color(0xff0000))
        else:
            em = discord.Embed(title="Autorole is enabled for this guild.", color = discord.Color(0x32ff00))
            rol = discord.utils.get(ctx.guild.roles, id=exists)
            em.add_field(name="Current role:", value=rol.mention)
        await ctx.send(embed=em)

    @autorole.command(name="enable")
    @commands.has_permissions(administrator=True)
    async def _enable(self, ctx, role: discord.Role=None):
        exists = dbinteraction.dbexec("SELECT role from serverdata WHERE server_id = ?", (ctx.guild.id,))
        print(f"status, role : enabled {role.id}"")
        try:
            if role==None:
                await ctx.send("No role provided")
            else:
                if (exists!=None):
                    dbinteraction.dbexec("UPDATE serverdata SET role = ?",(role.id,))
                else:
                    dbinteraction.dbexec("INSERT INTO serverdata VALUES(?,?)",(ctx.guild.id, role.id,))
                em = discord.Embed(title="", color= discord.Color(0x32ff00))
                em.add_field(name="Autorole enabled", value=f"Current role: {(role.mention)}")
                await ctx.send(embed=em)

        except (Exception) as e:
            print(e)
    
    @autorole.command(name="disable")
    @commands.has_permissions(administrator=True)
    async def _disable(self, ctx):
        exists = dbinteraction.dbexec("SELECT role from serverdata WHERE server_id = ?", (ctx.guild.id,))
        print('disab')
        if(exists!=None):
            try:
                dbinteraction.dbexec("DELETE FROM serverdata WHERE server_id = ?", (ctx.guild.id,))
                await ctx.send("Autorole disabled")
            except(Exception) as e:
                print(e)
        else:
            await ctx.send("Autorole wasn't enabled for this guild.")


def setup(bot):
    bot.add_cog(ServerManagement(bot))