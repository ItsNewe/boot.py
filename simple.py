import discord
import requests
#import tweepy
import random
import psutil
import emoji
import string
import re
import time, datetime
from dbinteraction import *
from discord.ext import commands

#tck=dbexec("SELECT twConsKey FROM bottk")
#tcs=dbexec("SELECT twConsSec FROM bottk")
#tkk=dbexec("SELECT twTokKey FROM bottk")
#tks=dbexec("SELECT twTokSec FROM bottk")
#auth= tweepy.OAuthHandler(tck,tcs)
#auth.set_access_token(tkk,tks)
#tapi= tweepy.API(auth)

class Simple(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def sys(self, ctx):
        """Returns server system stats"""

        em = discord.Embed(title="System stats", type="rich", colour=discord.Colour(16711680))
        em.add_field(name="CPU", value=f"{psutil.cpu_percent()}%", inline=False)
        em.add_field(name="RAM :ram:", value=f"{psutil.virtual_memory()[2]}%", inline=False)
        #em.set_thumbnail(self.bot.avatar)
        await ctx.send(embed=em)

    @commands.command()
    async def ping(self, ctx):
        """Pong!"""

        await ctx.send("ws: `"+str(round(ctx.bot.latency*1000,3))+"ms`")

    @commands.command()
    async def neko(self, ctx):
        """OwO?"""

        response = requests.get("http://nekos.life/api/neko")
        print(f"Response: {response.status_code}")
        wrap = discord.Embed(title="", type="rich")
        wrap.set_image(url=response.json()["neko"])
        await ctx.send(embed=wrap)
    
    @commands.command()
    async def cat(self, ctx, g=None): #TODO Always sends the same image (API misuse prolly)
        """Meow"""

        r="/gif" if g=="g" else ""
        response = requests.get(f"http://cataas.com/cat{g}", verify=False)
        print(f"Response: {response.status_code}")
        wrap = discord.Embed(title="", type="rich")
        wrap.set_image(url="https://cataas.com/cat")
        await ctx.send(embed=wrap)

    @commands.command()
    async def dog(self, ctx, breed=None, subbreed=None):
        """Sends you a doggo picture"""

        try:
            if not breed:
                r= requests.get("https://dog.ceo/api/breeds/image/random")
            else:
                if(subbreed):
                    r = requests.get(f"https://dog.ceo/api/breed/{breed}/{subbreed}/images/random")
                else:
                    r = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
            em = discord.Embed(title=""
            )
            em.set_image(url=r.json()["message"])
            await ctx.send(embed = em)
        except:
            await ctx.send("Bad args\nIs the breed you're looking for a sub-breed?\n**Format:**`$dog [breed] [sub-breed]`\nBreeds list: https://dog.ceo/api/breeds/list/all")

            ###NOT WORKING, MY DUMBASS NEEDS TO FIND OUT HOW IT WORKS###
    # @commands.command()
    # async def twitteruser(self, ctx,a):
    #     if(a==None):
    #         await ctx.send("You need to provide a user.")
    #         return
    #     try:
    #         urlem="https://twitter.com/{}".format(a)
    #         user = tapi.get_user(a)

    #         wrap=discord.Embed(Title="Twitter user", type="rich", url=urlem, colour=discord.Colour.from_rgb(0,172,237))
    #         wrap.set_thumbnail(url=user.profile_image_url)
    #         wrap.add_field(name="Name", value=user.name)
    #         wrap.add_field(name="Tweets", value=user.statuses_count)
    #         wrap.add_field(name="Username", value="@{}".format(user.screen_name), inline=False)
    #         wrap.add_field(name="Followers", value=user.followers_count)
    #         wrap.add_field(name="Following", value=user.friends_count)
    #         wrap.add_field(name="Bio", value=user.description, inline=False)
    #         await ctx.send(embed=wrap)
    #     except(tweepy.TweepError):
    #         await ctx.send("User `{}` not found.".format(a))
    #         return
    #     except(Exception):
    #         await ctx.send("An error occured with the following message:```py\n{}```".format(Exception))
    #         return

    @commands.command()
    async def owo(self, ctx, *, text: commands.clean_content):
        """Wetuwns the given phwase in owospeak UwU"""

        replacement_table = { # Thanks luna for the rep table!
            r'[rl]': 'w',
            r'[RL]': 'W',
            r'n([aeiou])': 'ny\\1',
            r'N([aeiou])': 'Ny\\1',
            r'ove': 'uv'
        }
        kao=["OwO", "UwU", ":3"]
        r= random.randint(0,len(kao)-1)
        for regex, replace_with in replacement_table.items():
            text = re.sub(regex, replace_with, text)

        em = discord.Embed(title=f"{ctx.message.author.name} Says:")
        em.add_field(name='OwO', value=text+ " "+kao[r])
        em.set_thumbnail(url=ctx.message.author.avatar_url)
        await ctx.send(embed=em)

    @commands.command(aliases=['acc'])
    async def account(self, ctx):
        """Creates a Konata account (useful only for osu atm, interesting stuff is cooking)"""

        yesno=dbexec("SELECT * FROM users WHERE id=?", (ctx.message.author.id,))

        if yesno==None:
            v=(ctx.message.author.id, ctx.message.author.name)
            a=dbexec("INSERT INTO users VALUES (?,?,?,?)",(v, None, time.time(),), f=False)
            if a=="err":
                ctx.send("error")
            await ctx.send("Account created successfully <:NWKonataThumbsUp:445210207597887489>")
            return

        else:
            username1=dbexec('SELECT username FROM users WHERE id=?', ctx.message.author.id )
            osuname=dbexec('SELECT osuname FROM users WHERE id=?', ctx.message.author.id )
            creadate=dbexec('SELECT creatime FROM users WHERE id=?', ctx.message.author.id )
            em= discord.Embed(title=f"Account info for {ctx.message.author.name}", colour=discord.Color.blurple())
            em.add_field(name="Username", value=username1)
            if osuname:
                em.add_field(name="Osu! account", value=osuname)
            em.add_field(name="Creation date", value=datetime.datetime.fromtimestamp(creadate).strftime('%Y-%m-%d %H:%M'))
            em.set_thumbnail(url=ctx.message.author.avatar_url)
            await ctx.send(embed=em)

    @commands.command()
    async def invite(self, ctx):
        """Gives you the bot's invite link"""
        em = discord.Embed(title="Useful links", color=discord.Colour.red())
        em.add_field(name="\u200b", value="[Invite the bot in your server](https://discordapp.com/oauth2/authorize?client_id=366632492590956544&permissions=8&scope=bot)", inline=False)
        em.add_field(name="\u200b", value="[Join the support server](https://discord.gg/YPAqxX9)", inline=False)
        em.add_field(name="\u200b", value="[Vote for this bot on DBL](https://discordbots.org/bot/366632492590956544)", inline=False)
        em.set_footer(text=em.timestamp, icon_url="https://cdn.discordapp.com/avatars/366632492590956544/e33fb154663f5a63138d934224b47c7d.png")
        await ctx.send(embed=em)

    @commands.command()
    async def avatar(self, ctx, *, usr: discord.Member = None):
        if(usr is None):
            usr = ctx.message.author
        await ctx.send(usr.avatar_url)
        
        
    
def setup(bot):
    bot.add_cog(Simple(bot))
