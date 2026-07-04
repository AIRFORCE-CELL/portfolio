"""
配置管理
"""

import os
from dataclasses import dataclass, field

from dotenv import load_dotenv

load_dotenv()


@dataclass
class Settings:
    """全局配置"""

    # API
    api_key: str = os.getenv("API_KEY", "dev-key-change-me")
    host: str = os.getenv("HOST", "0.0.0.0")
    port: int = int(os.getenv("PORT", "8000"))

    # 数据库 (SQLite 默认，生产换 PostgreSQL)
    database_url: str = os.getenv(
        "DATABASE_URL", "sqlite+aiosqlite:///./data/scraper.db"
    )

    # 采集设置
    default_timeout: int = int(os.getenv("DEFAULT_TIMEOUT", "30"))
    max_concurrent: int = int(os.getenv("MAX_CONCURRENT", "5"))
    user_agent: str = os.getenv(
        "USER_AGENT",
        "Mozilla/5.0 (compatible; ScraperBot/1.0; +https://example.com/bot)",
    )
    respect_robots: bool = os.getenv("RESPECT_ROBOTS", "true").lower() == "true"

    # 缓存 (Redis 可选)
    redis_url: str | None = os.getenv("REDIS_URL")

    # 浏览器渲染 (Playwright)
    use_browser: bool = os.getenv("USE_BROWSER", "true").lower() == "true"
    headless: bool = os.getenv("HEADLESS", "true").lower() == "true"


settings = Settings()
