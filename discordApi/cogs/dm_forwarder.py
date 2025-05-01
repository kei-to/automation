import discord
from discord.ext import commands

class DMForwarder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_name = "ボットの独り言"
        self.category_name = "ボットの遊び場"

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if isinstance(message.channel, discord.DMChannel):
            print(f"DM受信: {message.author}: {message.content}")

            # Botとユーザーが共通で所属しているサーバーを抽出
            mutual_guilds = [
                guild for guild in self.bot.guilds
                if guild.get_member(message.author.id) is not None
            ]

            if len(mutual_guilds) == 0:
                await message.channel.send("⚠️ あなたが所属しているサーバーの中に、Botが存在するものが見つかりませんでした。")
                return

            if len(mutual_guilds) > 1:
                await message.channel.send("⚠️ 複数の共通サーバーに所属しているため、どのサーバーに投稿すべきか判断できません。")
                return

            guild = mutual_guilds[0]

            # カテゴリ取得または作成
            category = discord.utils.get(guild.categories, name=self.category_name)
            if not category:
                category = await guild.create_category(self.category_name)
                print(f"カテゴリ '{self.category_name}' を作成しました。")

            # チャンネル取得または作成
            channel = discord.utils.get(category.text_channels, name=self.channel_name)
            if not channel:
                channel = await guild.create_text_channel(self.channel_name, category=category)
                print(f"チャンネル '{self.channel_name}' を作成しました。")

            # Embedメッセージ作成
            embed = discord.Embed(
                title="📩 新しいDMメッセージ",
                description=message.content,
                color=discord.Color.blue()
            )
            # embed.set_author(
            #     name=str(message.author),
            #     icon_url=message.author.avatar.url if message.author.avatar else discord.Embed.Empty
            # )

            await channel.send(embed=embed)
            await message.channel.send(f"✅ メッセージを **{guild.name}** に転送しました。")

async def setup(bot):
    await bot.add_cog(DMForwarder(bot))