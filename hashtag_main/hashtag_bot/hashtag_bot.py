# bot/hashtag_bot.py

import logging
from discord.ext import tasks
import discord

logger = logging.getLogger(__name__)

class HashtagBot:
    def __init__(self, bot, twitter_client, target_category_name="Twitter連携"):
        self.bot = bot
        self.twitter_client = twitter_client
        self.target_category_name = target_category_name
        self.posted_tweet_ids = set()

        self.fetch_loop.start()

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
