"""
AI 对话模块 — 支持 OpenAI / Claude / 本地模型
"""

import logging
from typing import Optional

log = logging.getLogger("bot.ai")


class AIChat:
    """AI 对话管理器"""

    def __init__(self, config):
        self.config = config
        self.client = None
        if config.openai_api_key:
            self._init_openai()

    def _init_openai(self):
        """初始化 OpenAI 客户端"""
        try:
            from openai import AsyncOpenAI

            self.client = AsyncOpenAI(api_key=self.config.openai_api_key)
            log.info("✅ OpenAI 客户端已初始化")
        except ImportError:
            log.warning("⚠️ 未安装 openai 包，AI 功能不可用。pip install openai")

    async def chat(self, message: str, context: Optional[list[dict]] = None) -> str:
        """发送对话并获取回复"""
        if not self.client:
            return "⚠️ AI 功能未配置（需要设置 OPENAI_API_KEY）"

        messages = [{"role": "system", "content": self.config.system_prompt}]
        if context:
            messages.extend(context[-10:])  # 保留最近 10 条上下文
        messages.append({"role": "user", "content": message})

        try:
            response = await self.client.chat.completions.create(
                model=self.config.openai_model,
                messages=messages,
                max_tokens=1000,
                temperature=0.7,
            )
            return response.choices[0].message.content
        except Exception as e:
            log.error(f"AI 请求失败: {e}")
            return "抱歉，我暂时无法回复。请稍后再试。"
