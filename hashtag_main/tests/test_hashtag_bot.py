import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from hashtag_bot.hashtag_bot import HashtagBot
from hashtag_bot.twitter_client import TwitterClient

class TestHashtagBot(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.bot = MagicMock()
        self.twitter_client = AsyncMock(spec=TwitterClient)
        self.hashtag_bot = HashtagBot(self.bot, self.twitter_client)

        # チャンネルモックとAsyncMockの送信メソッド
        self.mock_channel = MagicMock()
        self.mock_channel.name = "#news"
        self.mock_channel.id = 123
        self.mock_channel.category = MagicMock()
        self.mock_channel.category.name = "Twitter連携"
        self.mock_channel.send = AsyncMock()  # ← await に対応！

        self.mock_guild = MagicMock()
        self.mock_guild.text_channels = [self.mock_channel]

    async def test_extract_hashtags_from_channels(self):
        hashtags = self.hashtag_bot.extract_hashtags([self.mock_channel])
        self.assertEqual(hashtags, ['#news'])

    async def test_ignore_invalid_channel_names(self):
        self.mock_channel.name = "general"  # '#'なし
        hashtags = self.hashtag_bot.extract_hashtags([self.mock_channel])
        self.assertEqual(hashtags, [])

    async def test_fetch_and_post_success(self):
        self.twitter_client.fetch_latest_tweets.return_value = [
            {"id": "tweet1", "text": "テストツイート"}
        ]
        self.hashtag_bot.posted_tweet_ids = set()

        await self.hashtag_bot.fetch_and_post(["#news"], self.mock_channel)

        self.twitter_client.fetch_latest_tweets.assert_awaited_once_with("#news")
        self.mock_channel.send.assert_awaited_once_with("テストツイート")  # ← assert_awaited

    async def test_fetch_and_post_duplicate(self):
        self.twitter_client.fetch_latest_tweets.return_value = [
            {"id": "tweet1", "text": "テストツイート"}
        ]
        self.hashtag_bot.posted_tweet_ids = {"tweet1"}

        await self.hashtag_bot.fetch_and_post(["#news"], self.mock_channel)

        self.mock_channel.send.assert_not_awaited()  # ← OK now

    async def test_api_error_logs_but_does_not_retry(self):
        self.twitter_client.fetch_latest_tweets.side_effect = Exception("API error")

        with self.assertLogs(level="ERROR") as log:
            await self.hashtag_bot.fetch_and_post(["#news"], self.mock_channel)

        self.assertTrue(any("API error" in message for message in log.output))