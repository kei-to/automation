# main.py

import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from hashtag_bot.twitter_client import TwitterClient
from hashtag_bot.hashtag_bot import HashtagBot

# .envファイルの読み込み
load_dotenv()

TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Intentsの設定（メンバーやチャンネルの監視を有効にする）
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True  # メッセージ取得に必要（Bot設定でもONにする）

# Botインスタンスの作成
bot = commands.Bot(command_prefix="!", intents=intents)

# Botが起動したときの処理
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("------")

# HashtagBotを起動
@bot.event
async def setup_hook():
    twitter_client = TwitterClient()
    HashtagBot(bot, twitter_client)

# Botの起動
if __name__ == "__main__":
    if TOKEN is None:
        raise ValueError("DISCORD_BOT_TOKEN が .env に設定されていません")
    bot.run(TOKEN)