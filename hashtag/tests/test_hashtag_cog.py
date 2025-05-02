import unittest
from unittest.mock import MagicMock, AsyncMock
from discord.ext import commands
from discord import Intents  # ← 追加
from hashtag_bot.cogs.hashtag_cog import HashtagCog

class TestHashtagCog(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        intents = Intents.default()
        intents.message_content = True  # ← 必要に応じて
        self.bot = commands.Bot(command_prefix="!", intents=intents)
        self.cog = HashtagCog(self.bot)

        # チャンネルモック
        self.mock_channel = MagicMock()
        self.mock_channel.name = "#news"
        self.mock_channel.id = 123
        self.mock_channel.category = MagicMock()
        self.mock_channel.category.name = "Twitter連携"
        self.mock_channel.send = AsyncMock()

    async def test_extract_hashtags(self):
        result = self.cog.extract_hashtags([self.mock_channel])
        self.assertEqual(result, ["#news"])

    async def test_extract_hashtags_ignores_non_matching(self):
        self.mock_channel.name = "general"  # '#'がついてない
        result = self.cog.extract_hashtags([self.mock_channel])
        self.assertEqual(result, [])

    async def test_fetch_and_post_success(self):
        self.cog.twitter_client.fetch_latest_tweets = AsyncMock(return_value=[
            {"id": "1", "text": "ツイート1"},
            {"id": "2", "text": "ツイート2"},
        ])
        self.cog.posted_tweet_ids = set()

        await self.cog.fetch_and_post(["#news"], self.mock_channel)

        self.assertEqual(self.mock_channel.send.await_count, 2)
        self.mock_channel.send.assert_any_await("ツイート1")
        self.mock_channel.send.assert_any_await("ツイート2")

    async def test_fetch_and_post_duplicate_filtered(self):
        self.cog.twitter_client.fetch_latest_tweets = AsyncMock(return_value=[
            {"id": "1", "text": "ツイート1"},
        ])
        self.cog.posted_tweet_ids = {"1"}

        await self.cog.fetch_and_post(["#news"], self.mock_channel)

        self.mock_channel.send.assert_not_awaited()

    async def test_fetch_and_post_handles_error(self):
        self.cog.twitter_client.fetch_latest_tweets = AsyncMock(side_effect=Exception("API error"))

        with self.assertLogs(level="ERROR") as log:
            await self.cog.fetch_and_post(["#news"], self.mock_channel)

        self.assertTrue(any("API error" in msg for msg in log.output))

