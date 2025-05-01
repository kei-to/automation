# ファイル: cogs/dm_channel_creator.py
import discord
from discord.ext import commands
import os

class DMChannelCreator(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.category_name = "個別チャンネル"
        self.category_id = None  # ← ここにIDを保持

    # ★ チェック関数を作る
    async def is_admin(interaction: discord.Interaction) -> bool:
        # 管理者権限を持っているかを確認
        return interaction.user.guild_permissions.administrator

    @commands.Cog.listener()
    async def on_ready(self):
        print('ログインしました')
        new_activity = f"テスト"
        await self.bot.change_presence(activity=discord.Game(new_activity))
        await self.bot.tree.sync()  # コマンドを同期！

    @discord.app_commands.command(name='createdmchannel', description='Create or reuse a personal DM channel')
    @discord.app_commands.check(is_admin)  # ★ここで管理者だけ許可
    async def create_dm_channel(self, interaction: discord.Interaction):
        for guild in self.bot.guilds:
            # カテゴリ検索
            category = discord.utils.get(guild.categories, name=self.category_name)

            if category:
                print(f"カテゴリ {self.category_name} は既に存在します（ID: {category.id}）")
            else:
                print(f"カテゴリ {self.category_name} が見つかりません、作成します")
                category = await guild.create_category(name=self.category_name)
            # IDを保持
            self.category_id = category.id

        created = []

        async for member in interaction.guild.fetch_members():
            if member.bot:
                continue

            user_id = member.id
            channel_name = f"{member.name}さん"
            user_topic = f"User ID: {user_id}"

            # topicベースで重複チェック
            exists = any(
                ch.topic and user_topic in ch.topic
                for ch in category.text_channels
            )
            if exists:
                continue

            permission = {
                interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.guild.me: discord.PermissionOverwrite(read_messages=True),
                interaction.guild.owner: discord.PermissionOverwrite(read_messages=True),
                member: discord.PermissionOverwrite(read_messages=True),
            }

            await category.create_text_channel(
                name=channel_name,
                overwrites=permission,
                topic=user_topic
            )
            created.append(channel_name)

        if created:
            await interaction.response.send_message(f"{len(created)}件のチャンネルを作成しました。", ephemeral=True)
        else:
            await interaction.response.send_message("作成対象はありませんでした。", ephemeral=True)

    @create_dm_channel.error
    async def create_dm_channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, discord.app_commands.errors.CheckFailure):
            await interaction.response.send_message("🚫 あなたにはこのコマンドを実行する権限がありません。", ephemeral=True)
        else:
            raise error  # 他のエラーはそのまま上げる

# setup関数（必須）
async def setup(bot):
    await bot.add_cog(DMChannelCreator(bot))
