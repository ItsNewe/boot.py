import discord
import requests
import dbinteraction
from discord.ext import commands

class Osu(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		self.k = dbinteraction.dbexec("osuKey", log=True)

	@commands.command()
	async def osu(self, ctx, user=None, raw=False):
		"""Returns Osu! stats for a given user."""

		if user==None:
			try:
				a=dbinteraction.dbexec("SELECT osuname FROM users WHERE id = ?", (ctx.message.author.id,))
				if a!=None:
					user=a
				else:
					return
			except(Exception) as e:
				await ctx.send("An error occured")
				print(e)
				return
		try:
			response = requests.get(f"https://osu.ppy.sh/api/get_user?k={self.k}&u={user}&mode=0&type=string")
			rj = response.json()[0]
			if(raw):
				await ctx.send(f"**RAW JSON DATA**\n```json\nrj}```")
			else:
				em = discord.Embed(title=f"Osu profile for {rj["username"]}", color=discord.Color(0xFD00FD))
				em.set_thumbnail(url=f"https://a.ppy.sh/{rj["user_id"]}")
				em.add_field(name="Level", value=round(float(rj["level"]), 0))
				em.add_field(name="Country", value=rj["country"])
				em.add_field(name="PP", value=round(float(rj["pp_raw"]), 0))
				em.add_field(name="Rank", value=f"#{rj["pp_rank"]}")
				em.add_field(name="Accuracy", value=f"{round(float(rj["accuracy"]), 2)}%")
				em.add_field(name="Play count", value=rj["playcount"])
				em.add_field(name="SS ranks", value=rj["count_rank_ss"])
				em.add_field(name="S ranks", value=rj["count_rank_s"])
				em.add_field(name="A ranks", value=rj["count_rank_a"])
				em.set_footer(text=f"Requested by {ctx.message.author}")
				await ctx.send(embed=em)
		except:
			await ctx.send("The provided user could not be found.")
	
	@commands.command()
	async def osulink(self, ctx, user=""):
		"""Links the given osu username to your Konata account"""
		try:
			a=dbinteraction.dbexec("SELECT osuname FROM users WHERE id = ?", (ctx.message.author.id,))
			if a!=None:
				t = (user,)
				ch= ctx.message.author
				dbinteraction.dbexec("UPDATE users SET osuname = ? WHERE id = ? ", (user, ctx.message.author.id,), f=False)
				await ctx.send(f"Changed your Osu!username to {user}")
			else:
				ch= ctx.message.author
				dbinteraction.dbexec("INSERT INTO users values(?,?,?)", (ctx.message.author.id, ch-ch[3:], user,), f=False)
		except:
			print("err")

def setup(bot):
	bot.add_cog(Osu(bot))

	