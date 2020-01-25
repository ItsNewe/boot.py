import discord
from discord.ext import commands
import requests
from datetime import datetime
from lxml import etree

class atc(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	
	def baseRequest(self, queryString):
		r = requests.get(f"http://flightgear-atc.alwaysdata.net/dev2017_04_28.php?{queryString}")
		parsed= etree.fromstring(r.content)
		rDict={}
		for child in parsed:
			rDict[etree.tostring(child.tag)]=etree.tostring(child.attrib)
		
		if rDict['code']:
			return 1
		else:
			return rDict

	@commands.command(aliases=["airport", "iscontrolled"])
	async def isAirportControlled(self, ctx, airport: str, date=None):
		now = datetime.now()
		a = now.strftime("%Y-%m-%d")
		b = now.strftime("%H:%M:%S")
		b = self.baseRequest(f"isAirportControlled&airport={airport}&date={a}&time={b}")
		if b !=1:
			color=0x1aff00 if b['isControlled']==1 else 0xff0000
			message="Controlled" if b['isControlled']==1 else "Uncontrolled"

			em = discord.Embed(title="", color=discord.Color(color))
			em.add_field(name=f"{b['airport'].upper()} is currently", value=message)
			await ctx.send(embed=em)
		else:
			await ctx.send('error')


def setup(bot):
    bot.add_cog(atc(bot))
