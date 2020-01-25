import discord
from discord.ext import commands
from pybooru import Danbooru
from dbinteraction import *
import re
import requests


def doALrequest(q: str, v: dict):
    r = requests.post('https://graphql.anilist.co',
                      json={'query': q, 'variables': v})
    return r.json()


class anime(commands.Cog):
    def __init__(self, bot):
        self.client = Danbooru(
            'danbooru', api_key=dbexec('danbooruKey', log=True))
        self.bot = bot

    @commands.command(aliases=['dnb'])
    async def danbooru(self, ctx, *, tags1: str):
        """Gets an image from Danbooru, tags must be valid tags on the website"""
        # replacement_table = {
        #    r' ': '_',
        #    r',': ' '
        # }
        # for regex, replace_with in replacement_table.items():
        #    tags1 = re.sub(regex, replace_with, tags1)

        try:
            # Create post object
            class post:
                def __init__(self, data):
                    self.id = data[0]['id']
                    self.score = data[0]['score']
                    self.rating = data[0]['rating']
                    self.img = data[0]['file_url']
                    self.uploadername = data[0]['uploader_name']
            try:
                while True:
                    counter = 1
                    print("Attempt {}".format(counter))
                    data = self.client.post_list(
                        limit=1, tags=tags1, random=True)
                    if (not data):
                        await ctx.send("Invalid tag*(s)*")
                        return

                    bnd = post(data)
                    if(bnd.rating == 's'):
                        break

            except(Exception) as e:
                print(e)
                await ctx.send('An error occured')
                return

            em = discord.Embed(title="Search result", url=bnd.img)
            em.add_field(name='Uploaded by',
                         value=bnd.uploadername, inline=True)
            em.add_field(name="Score", value=bnd.score, inline=True)
            em.set_image(url=bnd.img)
            await ctx.send(embed=em)

        except(Exception) as e:
            print(e)

    @commands.command()
    async def charinfo(self, ctx, *, name: str):
        """Gets info about anime/manga character"""
        content = doALrequest(q="""query ($s: String, $page: Int) {
			Page(page: $page, perPage: 1) {
				pageInfo {
				total
				currentPage
				lastPage
				hasNextPage
				perPage
				}
				characters(search: $s) {
				name{
					first
					last
					native
					alternative
				}
				image{
					large
				}
				description(asHtml: false)
				}
			}
			}""", v={"s": name})
        if content['data']['Page']['characters']:
            c = content['data']['Page']['characters'][0]
            em = discord.Embed(
                title=f"{c['name']['first']} {c['name']['last']if c['name']['last'] is not None else ''} ({c['name']['native']})")
            em.add_field(name='Description', value=c['description'] if len(
                c['description']) < 1024 else c['description'][0:1023], inline=True)
            em.set_image(url=c['image']['large'])
            await ctx.send(embed=em)
        else:
            await ctx.send("This character doesn't exist")

    @commands.command(aliases=['ainfo', 'anime'])
    async def animeinfo(self, ctx, *, name: str):
        """Gets info about an anime"""
        content = doALrequest(q="""query ($s: String, $page: Int) {
        Page(page: $page, perPage: 1) {
            pageInfo {
            total
            currentPage
            lastPage
            hasNextPage
            perPage
            }
            media(search: $s) {
            title {
                romaji
                english
                native
            }
            status
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            episodes
            duration
            source
            genres
            averageScore
            popularity
            coverImage {
                large
            }
            description(asHtml: false)
            }
        }
        }""", v={"s": name})
        if content['data']['Page']['media']:
            c = content['data']['Page']['media'][0]
            em = discord.Embed(
                title=f"{c['title']['english'] if c['title']['english'] else ''} |  {c['title']['romaji']} ({c['title']['native']})")
            em.add_field(name=c['status'], value='lol')
            em.add_field(name="Episodes", value=f"{c['episodes']}", inline=True)
            em.add_field(name="Duration", value=f"{c['duration']}min per ep", inline=True)
            em.add_field(name='Description', value=c['description'] if len(
                c['description']) < 1024 else c['description'][0:1023], inline=True)
            em.set_image(url=c['coverImage']['large'])
            await ctx.send(embed=em)
        else:
            await ctx.send("This character doesn't exist")


def setup(bot):
    bot.add_cog(anime(bot))
