import discord
from discord.ext import commands
import requests

class ImgManip(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	def baseRequest(endpoint: string, images: list=None, args=None):
		requestBody = {}
		requestBody['images'] = images if images
		requestbody['args'] = args if args
		r = requests.post(f"https://fapi.wrmsr.io/{endpoint}", data=requestBody, header={"Authorization": "Bearer 56905ad15fcc726ab02ef36b1237caa6"})
		return r.response
	
	@commands.command()
	async def supreme(self, ctx, img:str=None):
		i=img if img else ctx.message.attachements[0]['url']
		if not i:
			return
		r = baseRequest('Supreme', [i])
		await ctx.send(r)


def setup(bot):
	bot.add_cog(ImgManip(bot))