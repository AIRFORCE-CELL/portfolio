# 🤖 Discord Bot — 智能社群机器人

**生产级 Discord 机器人框架**，开箱即用。从接单到交付，30 分钟搞定定制化需求。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🧠 AI 对话 | 接入 OpenAI GPT-4o / Claude，在指定频道自动回复 |
| 🛡️ 自动审核 | 违禁词过滤 + 自动删消息，无需人工盯群 |
| 👋 欢迎系统 | 新成员加入自动发送欢迎消息 |
| 📊 投票 & 统计 | !poll 创建投票、!stats 查看服务器数据 |
| 🔨 管理命令 | !clear 批量删消息、!kick / !ban 成员管理 |
| 🐳 Docker 部署 | 一条命令上线，支持多服务器 |

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置
cp .env.example .env
# 编辑 .env，填入 DISCORD_TOKEN（必填）和 OPENAI_API_KEY（可选）

# 3. 启动
python -m bot
```

### Docker 部署

```bash
docker compose up -d
```

## 📋 命令列表

| 命令 | 权限 | 说明 |
|------|------|------|
| `!ping` | 所有人 | 延迟测试 |
| `!ask <问题>` | 所有人 | 向 AI 提问 |
| `!poll "标题" 选项1 选项2` | 所有人 | 创建投票 |
| `!serverinfo` | 所有人 | 查看服务器信息 |
| `!stats` | 所有人 | 机器人统计 |
| `!clear <数量>` | 管理消息 | 批量删除消息 |
| `!kick @用户` | 踢人 | 踢出成员 |
| `!ban @用户` | 封禁 | 封禁成员 |

## 🛠️ 技术栈

`Python 3.11` · `discord.py 2.x` · `OpenAI API` · `Docker`

## 💰 定制服务

需要定制功能？支持但不限于：

- Web3 / NFT 集成
- 游戏化等级系统
- 多语言支持
- 自定义 API 对接
- 仪表盘后台

📧 联系：1653526777@QQ.com
