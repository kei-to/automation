import discord
from discord.ext import commands
import os

class DMForwarder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.guild_id = int(os.getenv('GUILD_ID'))
        self.channel_id = int(os.getenv('CHANNEL_ID'))
        self.category_id = int(os.getenv('CATEGORY_ID'))

    @commands.Cog.listener()
    async def on_message(self, message):
        # 自分自身のメッセージやBotのメッセージは無視
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            print(f"DM受信: {message.author}: {message.content}")

            guild = self.bot.get_guild(self.guild_id)
            if not guild:
                print("サーバーが見つかりません")
                return

            channel = guild.get_channel(self.channel_id)
            if not channel:
                print("チャンネルが見つかりません")
                return

            embed = discord.Embed(
                title="📩 新しいDMメッセージ",
                description=message.content,
                color=discord.Color.blue()
            )
            # embed.set_author(
            #     name=str(message.author),
            #     icon_url=message.author.avatar.url if message.author.avatar else None
            # )

            await channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DMForwarder(bot))