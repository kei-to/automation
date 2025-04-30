import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

# .envファイル読み込み
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

# Intent設定（メッセージ内容取得など必要）
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

# Botインスタンス作成
bot = commands.Bot(command_prefix="!", intents=intents)

# Cog読み込み
@bot.event
async def on_ready():
    print(f'Bot起動完了！: {bot.user}')
    await bot.load_extension('cogs.dm_forwarder')  # Cogを読み込む

# Bot起動
bot.run(TOKEN)