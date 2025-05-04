# hashtag_bot/cogs/hashtag_cog.py

import discord
import re
import logging
from discord.ext import commands, tasks
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


    def is_valid_hashtag(tag: str) -> bool:
        return re.fullmatch(r"[a-zA-Z0-9_ぁ-んァ-ヶ一-龥ー]+", tag) is not None
    
    @staticmethod
    def normalize_tag(raw_tag: str) -> str:
        """
        入力されたタグ文字列をTwitterのハッシュタグとして安全に使える形式に正規化する。
        - 全角・半角空白を削除
        - 記号類（絵文字や!@#など）を除去
        - アルファベット・数字・日本語のみ残す
        """
        # スペース除去（全角・半角）
        tag = raw_tag.replace(" ", "").replace("　", "")
        
        # 許可する文字: 英数字・日本語（ひらがな・カタカナ・漢字）・アンダースコア
        tag = re.sub(r"[^\wぁ-んァ-ヶ一-龥ー]", "", tag)

        return tag
    
    def extract_hashtags(self, channels):
        hashtags = []
        for channel in channels:
            print(f"[DEBUG] name={channel.name} | category={getattr(channel.category, 'name', None)}")

            # __で始まるチャンネル名だけを対象に（カテゴリ制限を外す）
            if channel.name.startswith("__"):
                hashtags.append(channel.name[2:])  # "__"除去してハッシュタグ扱い
        return hashtags

    @tasks.loop(minutes=1)
    async def fetch_loop(self):
        for guild in self.bot.guilds:
            for channel in guild.text_channels:
                if channel.name.startswith("__"):
                    hashtags = self.extract_hashtags([channel])
                    await self.fetch_and_post(hashtags, channel)

    async def fetch_and_post(self, hashtags, channel):
        for tag in hashtags:
            normalized = HashtagCog.normalize_tag(tag)
            if not normalized:
                logger.warning(f"[Skip] Invalid or empty tag after normalization: {repr(tag)}")
                continue

            try:
                logger.debug(f"[API] Fetching tweets for: #{normalized}")
                tweets = await self.twitter_client.fetch_latest_tweets(f"#{normalized}")

                for tweet in tweets:
                    if tweet["id"] not in self.posted_tweet_ids:
                        await channel.send(tweet["text"])
                        self.posted_tweet_ids.add(tweet["id"])

            except Exception as e:
                if "429" in str(e):
                    logger.warning(f"[RateLimit] Skipped #{normalized}: Twitter API rate limit hit.")
                elif "400" in str(e):
                    logger.error(f"[BadRequest] Twitter rejected query #{normalized} (original: {repr(tag)}).")
                else:
                    logger.error(f"Error fetching tweets for {tag}: {e}")


# setup関数（必須）
async def setup(bot):
    await bot.add_cog(HashtagCog(bot))