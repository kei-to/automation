# hashtag_bot/cogs/hashtag_cog.py

import discord
from discord.ext import commands, tasks
import logging
from ..twitter_client import TwitterClient

logger = logging.getLogger(__name__)

class HashtagCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.twitter_client = TwitterClient()
        self.posted_tweet_ids = set()
        self.target_category_name = "Twitter連携"
        self.fetch_loop.start()

    def cog_unload(self):
        self.fetch_loop.cancel()

    def extract_hashtags(self, channels):
        return [
            channel.name for channel in channels
            if channel.name.startswith("#") and channel.category and channel.category.name == self.target_category_name
        ]

    @tasks.loop(minutes=10)
    async def fetch_loop(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.category and channel.category.name == self.target_category_name and channel.name.startswith("#"):
                    hashtags = self.extract_hashtags([channel])
                    await self.fetch_and_post(hashtags, channel)

    async def fetch_and_post(self, hashtags, channel):
        for tag in hashtags:
            try:
                tweets = await self.twitter_client.fetch_latest_tweets(tag)
                for tweet in tweets:
                    if tweet["id"] not in self.posted_tweet_ids:
                        await channel.send(tweet["text"])
                        self.posted_tweet_ids.add(tweet["id"])
            except Exception as e:
                logger.error(f"Error fetching tweets for {tag}: {e}")