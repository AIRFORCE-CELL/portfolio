"""
配置管理 — 支持 .env 文件和环境变量
"""

import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# 自动加载 .env
load_dotenv(Path(__file__).parent.parent / ".env")


@dataclass
class Config:
    """全局配置"""

    discord_token: str
    command_prefix: str = "!"

    # AI 配置
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o-mini"
    ai_channel_ids: list[int] = field(default_factory=list)
    system_prompt: str = "你是一个友好、乐于助人的 Discord 机器人助手。"

    # 管理
    owner_ids: list[int] = field(default_factory=list)
    log_channel_id: Optional[int] = None
    welcome_channel_id: Optional[int] = None
    welcome_message: str = "欢迎 {user} 加入 {server}！🎉"

    # 审核
    banned_words: list[str] = field(default_factory=list)
    auto_moderate: bool = True

    @classmethod
    def from_env(cls) -> "Config":
        """从环境变量加载配置"""
        return cls(
            discord_token=os.environ["DISCORD_TOKEN"],
            command_prefix=os.getenv("COMMAND_PREFIX", "!"),
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            owner_ids=_parse_int_list(os.getenv("OWNER_IDS", "")),
            log_channel_id=_parse_int(os.getenv("LOG_CHANNEL_ID")),
            welcome_channel_id=_parse_int(os.getenv("WELCOME_CHANNEL_ID")),
            welcome_message=os.getenv("WELCOME_MESSAGE", "欢迎 {user} 加入 {server}！🎉"),
            banned_words=[
                w.strip() for w in os.getenv("BANNED_WORDS", "").split(",") if w.strip()
            ],
            auto_moderate=os.getenv("AUTO_MODERATE", "true").lower() == "true",
        )


def _parse_int(value: Optional[str]) -> Optional[int]:
    if value:
        return int(value)
    return None


def _parse_int_list(value: str) -> list[int]:
    if not value.strip():
        return []
    return [int(x.strip()) for x in value.split(",") if x.strip()]
