#-*- coding: utf-8 -*-
import discord
import logging
import sys, traceback
import random
import dbinteraction
import json
import requests
from discord.ext import commands
import asyncio
from subprocess import call
import schedule
from datetime import datetime
import watchdoggo
from apscheduler.schedulers.background import BackgroundScheduler
import pytz

commandcnt = 0
dog = watchdoggo.Doggo

bot = commands.AutoShardedBot(command_prefix='n$', pm_help=False)

logging.basicConfig(level=logging.INFO, \
	format='[%(asctime)s] %(levelname)s - [%(name)s] %(message)s')
log = logging.getLogger(__name__)

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def stats():
	global commandcnt
	print("Stats INIT")
	print("dog OK")
	dog.gather(len(bot.guilds), len(bot.users), dbinteraction.dbexec("SELECT COUNT(*) FROM serverdata"), commandcnt)
	dog.update()
	print("Dog done")
	commandcnt = 0

def servping():
	call(["curl", "-X POST", "--data" ,f"time={datetime.now().timestamp()}&servs{len(bot.guilds)}", "http://newe.space/konata/status/check"])
	print('[[[[[EMITED SERVER PING]]]]]')

sched = BackgroundScheduler(daemon=True, timezone="Europe/Paris")
sched.add_job(stats, 'cron', hour='1', minute='1')
sched.add_job(servping, 'cron', minute='10')
sched.start()

async def autogmchange():
	try:
		await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.guilds)} servers | n$help", url='https://twitch.tv/newe1337', state="Doing bot things", details="skrrt skrrt"))
	except:
		pass
	await asyncio.sleep(300)

## Events

@bot.event
async def on_ready():
	guilds=[]
	ard=random.randint(1,8)
	print(f"Logged in as {bot.user}, d.py V{discord.__version__}")
	for g in bot.guilds:
		guilds.append(g.name)
	print("-----------------------------------------------------\n\
	Connected to: {}\n-----------------------------------------------------".format(" | ".join(guilds)))
	bt=bot.loop.create_task(autogmchange())

@bot.event
async def on_message(message):
	await bot.process_commands(message)

@bot.event
async def on_command(ctx):
	global commandcnt
	commandcnt+=1
	print(f"{bcolors.WARNING} [COMMAND] | {ctx.message.author} : {ctx.message.clean_content[2:]} [{commandcnt}] {bcolors.ENDC}")
	dog.ddNewCommand()
	call(["curl", "--data" ,f"content=**__{ctx.message.author}__** : `{ctx.message.clean_content[2:]}`&username=Commande exécutée&avatar_url=https://cdn.discordapp.com/attachments/440454225961680896/440454482657017856/goodjob.gif", dbinteraction.dbexec("comhook", log=True)])


@bot.event
async def on_guild_join(guild):
	try:
		em = discord.Embed(title="Hello ໒( ●ᴥ ●)ʋ", color=discord.Color(0xff0000))
		em.set_thumbnail(url="https://cdn.discordapp.com/avatars/366632492590956544/e33fb154663f5a63138d934224b47c7d.png?size=1024")
		em.add_field(name="The name's Konata", value="A capable and experimental discord bot!\n\
		To see the list of my commands, type **__n$__help** <:NWKonataThumbsUp:445210207597887489>\n\
		If you like what i do, please consider [voting for this bot](https://discordbots.org/bot/366632492590956544) and suggest this bot around, it would help me a lot, thanks　(\*´▽｀\*)!")

		ch = guild.system_channel
		print(f"channel set: {ch}")
		if not ch:
			print("not ch")
			for c in guild.text_channels:
				if not c.permissions_for(guild.me).send_messages:
					print("ch test")
					continue
				ch = c
				print("ch found")
				break
		print("done")
		await ch.send(embed=em)

		try:
			payload = { "embeds": [ { "title": "Nouveau serveur", "color": 11468544, "footer": { "icon_url": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/3f/3fabd870d12b4301114bd6ffe9267b8eb560036d_full.jpg", "text": f"Total: {len(bot.guilds)} serveurs" }, "thumbnail": { "url": guild.icon }, "fields": [ { "name": "Nom", "value": guild.name, "inline": True }, { "name": "Membres", "value": len(guild.members), "inline": True }, { "name": "ID", "value": guild.id, "inline": False }  ]} ] }
			headers = { 'Content-Type': 'application/json' }
			response = requests.post(dbinteraction.dbexec("serverhook", log=True), data=json.dumps(payload), headers=headers)
			return response

		except(Exception) as e:
			print(e)
			call(["curl", "--data" ,f"content=Nom: *{guild.name}*\nID : `{guild.id}`\n Total: {len(bot.guilds)} serveurs&username=Nouveau serveur&avatar_url=https://cdn.discordapp.com/attachments/440454225961680896/440454482657017856/goodjob.gif", dbinteraction.dbexec("serverhook", log=True)])

	except(Exception) as e:
		print(e)

@bot.event
async def on_guild_remove(guild):
	try:
		payload = { "embeds": [ { "title": "Nouveau serveur", "color": 16711684, "footer": { "icon_url": "https://steamcdn-a.akamaihd.net/steamcommunity/public/images/avatars/3f/3fabd870d12b4301114bd6ffe9267b8eb560036d_full.jpg", "text": f"Total: {len(bot.guilds)} serveurs" }, "thumbnail": { "url": guild.icon }, "fields": [ { "name": "Nom", "value": guild.name, "inline": True }, { "name": "Membres", "value": len(guild.members), "inline": True }, { "name": "ID", "value": guild.id, "inline": False }  ]} ] }
		headers = { 'Content-Type': 'application/json' }
		response = requests.post(dbinteraction.dbexec("serverhook", log=True), data=json.dumps(payload), headers=headers)
		return response
	except:
		print('guild leave, ms fail')
		call(["curl", "--data" ,f"content=Nom: *{guild.name}*\nID : `{guild.id}`\n Total: {len(bot.guilds)} serveurs&username=Serveur quitté&avatar_url=https://cdn.discordapp.com/attachments/440454225961680896/440454482657017856/goodjob.gif", dbinteraction.dbexec("serverhook", log=True)])
		
@bot.event
async def on_member_join(member):
	a=dbinteraction.dbexec("SELECT role FROM serverdata WHERE server_id = ?", (member.guild.id,))
	if a!=None:
		role = discord.utils.get(member.guild.roles, id=a)
		await member.add_roles(role, reason="[KONA] Autorole")

@bot.event
async def on_member_ban(guild, user):
	print(f"**{user.name}** has been banned!")

## Core commands
@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension_name : str):
	try:
		bot.load_extension(extension_name)
	except (AttributeError, ImportError) as e:
		await ctx.message.add_reaction('🈲')
		await ctx.send(f"```py\n{type(e).__name__}: {str(e)}\n```")
		return
	await ctx.message.add_reaction('🉑')

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension_name : str):
	try:
		bot.unload_extension(extension_name)
	except (AttributeError, ImportError) as e:
		await ctx.message.add_reaction('🈲')
		await ctx.send(f"```py\n{type(e).__name__}: {str(e)}\n```")
		return
	await ctx.message.add_reaction('🉑')

@bot.command(aliases=["rl"], hidden=True)
@commands.is_owner()
async def reload(ctx, extension_name : str):
	try:
		bot.unload_extension(extension_name)
		bot.load_extension(extension_name)
	except (AttributeError, ImportError) as e:
		await ctx.message.add_reaction('🈲')
		await ctx.send(f"```py\n{type(e).__name__}: {str(e)}\n```")
		return
	await ctx.message.add_reaction('🉑')

initial_extensions = ['simple', "admin", "osu", "audio", "anime", "owner", "dbotsapi", "servmgmt"]
if __name__ == "__main__":
	for extension in initial_extensions:
		try:
			bot.load_extension(extension)
		except Exception as e:
			exc = f"{type(e).__name__}: {e}"
			print(f"Failed to load extension `{extension}\n{exc}`")
			
print(f"{bcolors.OKGREEN}Logging in...!{bcolors.ENDC}")

bot.run(dbinteraction.dbexec("dstk", log=True))
