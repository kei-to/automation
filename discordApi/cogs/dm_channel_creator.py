# ファイル: cogs/dm_channel_creator.py
import discord
from discord.ext import commands
import os

class DMChannelCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.category_id = int(os.getenv('CATEGORY_ID'))  # ←安全に環境変数から取る

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
    async def create_dm_channel(self, interaction: discord.Interaction):
        category = interaction.guild.get_channel(self.category_id)
        if category is None:
            await interaction.response.send_message("カテゴリが見つかりませんでした。", ephemeral=True)
            return

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

# setup関数（必須）
async def setup(bot):
    await bot.add_cog(DMChannelCreator(bot))
