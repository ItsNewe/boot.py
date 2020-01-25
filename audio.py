import discord
from discord.ext import commands
import youtube_dl
import asyncio
import urllib.request
import urllib.parse
import random
from dbinteraction import *
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from ctypes.util import find_library

discord.opus.load_opus(find_library("opus"))
youtube_dl.utils.bug_reports_message = lambda: ''


#TODO audio stream ending abruptly (check yt api)
def yt_search(keyw):
    youtube = build('youtube', 'v3', developerKey=dbexec('ytkey', log=True))
    
    response = youtube.search().list(
        q=keyw,
        part='id,snippet',
        type='video',
        maxResults=1
    ).execute()

    video = {
        'vidid' : response['items'][0]['id']['videoId'],
        'titre' : response['items'][0]['snippet']['title'],
        'thumb' : response['items'][0]['snippet']['thumbnails']['default']['url'],
        'description' : response['items'][0]['snippet']['description'],
        'chaine' : response['items'][0]['snippet']['channelTitle']
    }
    return video

gifs=["https://cdn.discordapp.com/attachments/440454225961680896/448145641965617162/giphy.gif",
"https://cdn.discordapp.com/attachments/440454225961680896/440454431897550848/dancingdoggo.gif",
"https://cdn.discordapp.com/attachments/440454225961680896/440454386557255681/curry.gif",
"https://cdn.discordapp.com/attachments/440454225961680896/450742971659452432/momitr.gif",]

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.9):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)
    
class Audio(commands.Cog):
    def __init__(self,bot):
        self.bot=bot
        self.message=None
        self.playing=None
        self.title=None

    def playembed(self, ctx, video, url=None):
        em= discord.Embed(title=video['titre'], color=0xff0000)
        em.set_author(name="Now playing:", icon_url=ctx.message.author.avatar_url)
        em.set_thumbnail(url=video['thumb'])
        self.message = em
        return em


    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx, channel=None):
        """Brings the bot to your voice channel"""

        if ctx.message.author.voice.channel != None:
            channel=ctx.message.author.voice.channel
            if ctx.voice_client is not None:
                return await ctx.voice_client.move_to(channel)
            else:
                await channel.connect()
        else:
            await ctx.send("You are not in a voice channel")

    @commands.command()
    async def leave(self, ctx):
        """Kicks the bot out of your voice channel"""

        if ctx.voice_client is None:
            await ctx.send("I am not in a channel right now.")
        else:
            await ctx.voice_client.disconnect()
            
    @commands.command()
    async def skip(self, ctx):
        """Skips the currently playing song"""

        if ctx.message.author.voice.channel != None:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()
                await ctx.send("Skipped the current song.")
            else:
                ctx.send("Nothing is playing right now.")

    @commands.command()
    async def play(self, ctx, *, url: str):
        """Plays the specified song"""
        
        try:
            if(ctx.message.author.voice.channel != None):

                def autodisco(error):
                    coro = ctx.voice_client.disconnect()
                    fut = asyncio.run_coroutine_threadsafe(coro, self.bot.loop)
                    try:
                        fut.result()
                    except:
                        pass

                a=str
                async with ctx.typing():
                    try:
                        rd=random.randint(0,3)
                        em= discord.Embed(title="")
                        em.set_author(name="Searching...")
                        em.set_image(url=gifs[rd])
                        msg= await ctx.send(embed=em)

                        if (url[:7]!="http://" or url[:8]!="https://"):
                            vid = yt_search(url)
                            url= 'https://www.youtube.com/watch?v=' + vid['vidid']

                        if ctx.voice_client is None:
                            await ctx.message.author.voice.channel.connect()

                        if not ctx.voice_client.is_playing():
                            player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=True)
                            ctx.voice_client.play(player, after=autodisco)
                            pl=Audio.playembed(self, ctx, vid, url)
                            await msg.edit(content=None, embed=pl)

                            
                        else:
                            await ctx.send("The queuing system doesn't work yet, wait for the song to be over or skip it then play the one you wanted to play")
                            #queue.append(url)
                            #print(url)
                            #await ctx.send("Added the link to the queue")

                    except(Exception) as e:
                        await ctx.send("An error occured, this event has been transmitted to the developer")
                        print(f"!!!!!!!!!!!! YOUTUBE-DL FAIT ENCORE DE LA MERDE !!!!!!!!!!!!\nTraceback: {e}")

            else:
                await ctx.send('You need to be in a voice channel to do that')
        except(discord.ext.commands.MissingRequiredArgument):
            await ctx.send("Hey, give me something")
            return


def setup(bot):
    bot.add_cog(Audio(bot))
