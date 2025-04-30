# ファイル: main.py
import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

intents = discord.Intents.default()
intents.members = True

# .envのパスを決める
current_dir = os.getcwd()
if os.path.exists(os.path.join(current_dir, ".env")):
    # ルート直下に.envがあるなら
    env_path = os.path.join(current_dir, ".env")
elif os.path.exists(os.path.join(current_dir, "discordApi", ".env")):
    # configフォルダの中に.envがあるなら
    env_path = os.path.join(current_dir, "discordApi", ".env")
else:
    raise FileNotFoundError(".envファイルが見つかりませんでした")

load_dotenv(dotenv_path="../.env")

bot = commands.Bot(command_prefix="!", intents=intents)

async def main():
    async with bot:
        await bot.load_extension("cogs.dm_channel_creator")  # cog読み込み
        await bot.load_extension("cogs.dm_forwarder")  # cog読み込み
        await bot.start(os.getenv("DISCORD_TOKEN"))  # 環境変数からTOKEN取得して起動

asyncio.run(main())