import discord
from discord.ext import commands
import dbinteraction
from colour import Color as colorlib
from discord.utils import get


class ServerManagement(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.group(invoke_without_command=True)
	@commands.has_permissions(administrator=True)
	async def autorole(self, ctx):
		print(ctx.invoked_subcommand)
		exists = dbinteraction.dbexec(
			"SELECT role from serverdata WHERE server_id = ?", (ctx.guild.id,)
		)
		em = None
		if exists == None:
			em = discord.Embed(
				title="Autorole is disabled for this guild.",
				color=discord.Color(0xFF0000),
			)
		else:
			em = discord.Embed(
				title="Autorole is enabled for this guild.",
				color=discord.Color(0x32FF00),
			)
			rol = discord.utils.get(ctx.guild.roles, id=exists)
			em.add_field(name="Current role:", value=rol.mention)
		await ctx.send(embed=em)

	@autorole.command(name="enable")
	@commands.has_permissions(administrator=True)
	async def _enable(self, ctx, role: discord.Role = None):
		exists = dbinteraction.dbexec(
			"SELECT server_id from serverdata WHERE server_id = ?", (ctx.guild.id,)
		)
		print(f"status, role : enabled {role.id}")
		try:
			if role == None:
				await ctx.send("No role provided")
			else:
				if exists != None:
					dbinteraction.dbexec(
						"UPDATE serverdata SET role = ? WHERE server_id = ?",
						(role.id, ctx.guild.id),
					)
				else:
					dbinteraction.dbexec(
						"INSERT INTO serverdata VALUES(?,?, ?)",
						(ctx.guild.id, role.id, 0),
					)
				em = discord.Embed(title="", color=discord.Color(0x32FF00))
				em.add_field(
					name="Autorole enabled", value=f"Current role: {(role.mention)}"
				)
				await ctx.send(embed=em)

		except (Exception) as e:
			print(e)

	@autorole.command(name="disable")
	@commands.has_permissions(administrator=True)
	async def _disable(self, ctx):
		exists = dbinteraction.dbexec(
			"SELECT role from serverdata WHERE server_id = ?", (ctx.guild.id,)
		)
		print("disab")
		if exists != None:
			try:
				dbinteraction.dbexec(
					"DELETE FROM serverdata WHERE server_id = ?", (ctx.guild.id,)
				)
				await ctx.send("Autorole disabled")
			except (Exception) as e:
				print(e)
		else:
			await ctx.send("Autorole wasn't enabled for this guild.")

	@commands.group(invoke_without_command=True, aliases=["crole"])
	async def customrole(self, ctx, roleName: str = None, color: str = None):
		"""Creates a custom role, if enabled

        Parameters
        ------------
        name: str 
            The role's name. Use quotes if there are spaces

		color: str
			Color name, RGB values as "r,g,b", hex value
        """
		exists = dbinteraction.dbexec(
			"SELECT usrmaderole from serverdata WHERE server_id = ?", (ctx.guild.id,)
		)
		em = None
		if not exists:
			await ctx.send(
				embed=discord.Embed(
					title="Custom roles are disabled for this guild.",
					color=discord.Color(0xFF0000),
				)
			)
		else:
			if not roleName and exists:
				em = discord.Embed(
					title="Custom roles are enabled for this guild.",
					color=discord.Color(0xFF0000),
				)
			else:
				rid = dbinteraction.dbexec(
					"SELECT role FROM userCustomRole WHERE guildId = ? AND userID = ?",
					(ctx.guild.id, ctx.author.id,),
				)
				if rid:
					r = get(ctx.guild.roles, id=int(rid))
					await ctx.author.remove_roles(r)
					r.delete(
						reason="[KONA] Custom role replacement"
					)
				role = await ctx.guild.create_role(
					name=roleName,
					permissions=discord.Permissions.none(),
					color=discord.Color(int(colorlib(color).hex_l[1:], 16)) if color else discord.Color.default()
					if color
					else discord.Color.default(),
					hoist=True,
					mentionable=True,
					reason="[KONA] Custom role",
				)
				if rid:
					dbinteraction.dbexec(
					"UPDATE userCustomRole SET role = ? WHERE guildId = ? AND userID = ?", (
						role.id, ctx.guild.id, ctx.author.id,
					)
				)
				else:
					dbinteraction.dbexec(
					"INSERT into userCustomRole values(?,?,?)", (
						ctx.guild.id, ctx.author.id, role.id,
					))
				em = discord.Embed(
					title=f"You have been given the {roleName} role.",
					color=discord.Color.green(),
				)
				await ctx.author.add_roles(role, reason="[KONA] Custom role")

		await ctx.send(embed=em)

	@customrole.command(name="enable")
	@commands.has_permissions(administrator=True)
	async def _enablecustom(self, ctx, role: discord.Role = None):
		exists = dbinteraction.dbexec(
			"SELECT usrmaderole from serverdata WHERE server_id = ?", (ctx.guild.id,)
		)
		try:
			if exists != None:
				dbinteraction.dbexec(
					"UPDATE serverdata SET usrmaderole = 1 WHERE server_id = ?",
					(ctx.guild.id,),
				)
			else:
				dbinteraction.dbexec(
					"INSERT INTO serverdata VALUES(?,?,?)", (ctx.guild.id, None, 1,)
				)
			em = discord.Embed(
				title="Custom roles are enabled", color=discord.Color(0x32FF00)
			)
			await ctx.send(embed=em)

		except (Exception) as e:
			print(e)

	@customrole.command(name="disable")
	@commands.has_permissions(administrator=True)
	async def _disablecustom(self, ctx):
		exists = dbinteraction.dbexec(
			"SELECT usrmaderole from serverdata WHERE server_id = ?", (ctx.guild.id,)
		)
		print("disab")
		if exists != 0:
			try:
				dbinteraction.dbexec(
					"UPDATE serverdata SET usrmaderole = 0 WHERE server_id = ?",
					(ctx.guild.id,),
				)
				await ctx.send("Autorole disabled")
			except (Exception) as e:
				print(e)
		else:
			await ctx.send("Autorole wasn't enabled for this guild.")


def setup(bot):
	bot.add_cog(ServerManagement(bot))

