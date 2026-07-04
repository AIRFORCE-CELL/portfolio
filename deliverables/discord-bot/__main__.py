"""
Discord 机器人主入口
启动: python -m bot
"""

import asyncio
import logging
import os
import sys

import discord
from discord.ext import commands

from bot.ai import AIChat
from bot.config import Config
from bot.handlers import AdminCommands, CommunityCommands, Events

# ── 日志 ──────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger("bot")


class BotClient(commands.Bot):
    """机器人客户端"""

    def __init__(self, config: Config):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__(
            command_prefix=config.command_prefix,
            intents=intents,
            help_command=None,
        )
        self.config = config
        self.ai = AIChat(config)

    async def setup_hook(self):
        """加载模块"""
        await self.add_cog(Events(self))
        await self.add_cog(AdminCommands(self))
        await self.add_cog(CommunityCommands(self))
        log.info("✅ 所有模块加载完成")

    async def on_ready(self):
        log.info(f"🤖 {self.user} 已上线 | {len(self.guilds)} 个服务器")


async def main():
    config = Config.from_env()
    bot = BotClient(config)
    async with bot:
        await bot.start(config.discord_token)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        log.info("👋 机器人已关闭")
