import dbl
import discord
from discord.ext import commands

from dbinteraction import *
import aiohttp
import asyncio
import logging


class DiscordBotsOrgAPI(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.token = dbexec("dbotsApiKey", log=True)
        self.dblpy = dbl.Client(self.bot, self.token)
        self.bot.loop.create_task(self.update_stats())

    async def update_stats(self):
        while True:
            await asyncio.sleep(4)
            logger.info('updating info')
            try:
                await self.dblpy.post_server_count()
                votes = await self.dblpy.get_upvote_info()
                logger.info(f"Posted server count ({len(self.bot.guilds)})")
                logger.info(f"{len(votes)} votes")
            except Exception as e:
                logger.exception(f"Failed to post server count\n{type(e).__name__}: {e}")
            await asyncio.sleep(1800)


def setup(bot):
    global logger
    logger = logging.getLogger('bot')
    bot.add_cog(DiscordBotsOrgAPI(bot))