"""
事件处理 & 命令 — 社区功能、管理功能、事件监听
"""

import logging
from datetime import datetime, timedelta

import discord
from discord.ext import commands

log = logging.getLogger("bot.handlers")


# ══════════════════════════════════════════════════
#  事件监听
# ══════════════════════════════════════════════════

class Events(commands.Cog):
    """生命周期事件"""

    def __init__(self, bot):
        self.bot = bot
        self._spam_tracker: dict[int, list[datetime]] = {}  # 简单的防刷屏

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        """新成员加入"""
        config = self.bot.config
        if config.welcome_channel_id:
            channel = member.guild.get_channel(config.welcome_channel_id)
            if channel:
                msg = config.welcome_message.format(
                    user=member.mention, server=member.guild.name
                )
                await channel.send(msg)
        log.info(f"👋 {member} 加入了 {member.guild}")

    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member):
        """成员离开"""
        if self.bot.config.log_channel_id:
            channel = member.guild.get_channel(self.bot.config.log_channel_id)
            if channel:
                await channel.send(f"👋 {member.mention} 离开了服务器")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """消息处理 — AI 回复 + 审核"""
        if message.author.bot:
            return

        # 自动审核
        if self.bot.config.auto_moderate:
            await self._moderate(message)

        # AI 频道自动回复
        if (
            message.channel.id in self.bot.config.ai_channel_ids
            and self.bot.config.openai_api_key
        ):
            async with message.channel.typing():
                reply = await self.bot.ai.chat(message.content)
                if len(reply) > 1900:
                    # Discord 消息限制 2000 字符
                    chunks = [reply[i : i + 1900] for i in range(0, len(reply), 1900)]
                    for chunk in chunks:
                        await message.reply(chunk)
                else:
                    await message.reply(reply)

    async def _moderate(self, message: discord.Message):
        """简单的内容审核"""
        content_lower = message.content.lower()
        for word in self.bot.config.banned_words:
            if word.lower() in content_lower:
                try:
                    await message.delete()
                    log.warning(f"🗑️ 删除违规消息 from {message.author}: {word}")
                except discord.Forbidden:
                    pass
                return


# ══════════════════════════════════════════════════
#  管理命令
# ══════════════════════════════════════════════════

class AdminCommands(commands.Cog):
    """管理员命令"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        """延迟测试"""
        latency = round(self.bot.latency * 1000)
        await ctx.send(f"🏓 Pong! {latency}ms")

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx: commands.Context, amount: int = 10):
        """批量删除消息"""
        deleted = await ctx.channel.purge(limit=amount + 1)
        msg = await ctx.send(f"🗑️ 已删除 {len(deleted) - 1} 条消息")
        await msg.delete(delay=3)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx: commands.Context, member: discord.Member, *, reason="无"):
        """踢出成员"""
        await member.kick(reason=reason)
        await ctx.send(f"👢 {member.mention} 已被踢出 | 原因: {reason}")

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx: commands.Context, member: discord.Member, *, reason="无"):
        """封禁成员"""
        await member.ban(reason=reason)
        await ctx.send(f"🔨 {member.mention} 已被封禁 | 原因: {reason}")

    @commands.command(name="stats")
    async def stats(self, ctx: commands.Context):
        """服务器统计"""
        guild = ctx.guild
        embed = discord.Embed(
            title=f"📊 {guild.name} 统计",
            color=discord.Color.blue(),
            timestamp=datetime.now(),
        )
        embed.add_field(name="成员", value=guild.member_count, inline=True)
        embed.add_field(name="频道", value=len(guild.channels), inline=True)
        embed.add_field(name="角色", value=len(guild.roles), inline=True)
        embed.add_field(name="延迟", value=f"{round(self.bot.latency * 1000)}ms", inline=True)
        embed.add_field(name="服务器", value=len(self.bot.guilds), inline=True)
        embed.set_footer(text=f"ID: {guild.id}")
        await ctx.send(embed=embed)


# ══════════════════════════════════════════════════
#  社区命令
# ══════════════════════════════════════════════════

class CommunityCommands(commands.Cog):
    """社区互动命令"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ask")
    async def ask(self, ctx: commands.Context, *, question: str):
        """向 AI 提问"""
        if not self.bot.config.openai_api_key:
            await ctx.send("⚠️ AI 功能未配置")
            return
        async with ctx.typing():
            answer = await self.bot.ai.chat(question)
            await ctx.reply(answer[:1900])

    @commands.command(name="poll")
    async def poll(self, ctx: commands.Context, question: str, *options: str):
        """创建投票 !poll "问题" 选项1 选项2 选项3"""
        if len(options) < 2:
            await ctx.send("⚠️ 请提供至少 2 个选项")
            return
        if len(options) > 10:
            await ctx.send("⚠️ 最多 10 个选项")
            return

        emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        embed = discord.Embed(
            title=f"📊 {question}",
            description="\n".join(
                f"{emojis[i]} {opt}" for i, opt in enumerate(options)
            ),
            color=discord.Color.purple(),
        )
        embed.set_footer(text=f"由 {ctx.author.display_name} 发起")
        msg = await ctx.send(embed=embed)
        for i in range(len(options)):
            await msg.add_reaction(emojis[i])

    @commands.command(name="serverinfo")
    async def serverinfo(self, ctx: commands.Context):
        """服务器信息"""
        guild = ctx.guild
        embed = discord.Embed(
            title=guild.name,
            description=f"创建于 {guild.created_at.strftime('%Y-%m-%d')}",
            color=discord.Color.green(),
        )
        embed.set_thumbnail(url=guild.icon.url if guild.icon else None)
        embed.add_field(name="所有者", value=guild.owner.mention, inline=True)
        embed.add_field(name="成员", value=guild.member_count, inline=True)
        embed.add_field(name="频道", value=len(guild.channels), inline=True)
        embed.add_field(name="角色", value=len(guild.roles), inline=True)
        embed.add_field(name="Boosts", value=guild.premium_subscription_count, inline=True)
        await ctx.send(embed=embed)
