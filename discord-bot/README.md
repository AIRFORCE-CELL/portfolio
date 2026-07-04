# 🤖 Discord Bot SaaS Template

生产级 Discord 机器人模板，开箱即用。适合快速交付客户项目或二次开发。

## ✨ 功能

- ✅ **AI 对话** — 接入 OpenAI/Claude，支持频道自动回复和 `/ask` 命令
- ✅ **社区管理** — 欢迎新成员、投票、服务器信息
- ✅ **自动审核** — 违禁词过滤、自动删消息
- ✅ **管理命令** — 踢人/封禁/清屏/统计
- ✅ **多服务器支持** — 一个实例服务多个 Discord 服务器
- ✅ **Docker 一键部署** — 含 Dockerfile + docker-compose

## 🚀 快速开始

### 1. 创建 Discord 机器人
1. 访问 [Discord Developer Portal](https://discord.com/developers/applications)
2. 创建应用 → Bot → 获取 Token
3. 在 OAuth2 → URL Generator 中勾选 `bot` + `applications.commands`，生成邀请链接

### 2. 配置
```bash
cp .env.example .env
# 编辑 .env，填入 DISCORD_TOKEN 等信息
```

### 3. 运行

**方式一：直接运行**
```bash
pip install -r requirements.txt
python -m bot
```

**方式二：Docker（推荐生产环境）**
```bash
docker-compose up -d
```

## 📋 命令列表

| 命令 | 权限 | 说明 |
|------|------|------|
| `!ping` | 所有人 | 延迟测试 |
| `!ask <问题>` | 所有人 | 向 AI 提问 |
| `!poll "问题" 选项1 选项2` | 所有人 | 创建投票 |
| `!serverinfo` | 所有人 | 服务器信息 |
| `!stats` | 所有人 | 服务器统计 |
| `!clear <数量>` | 管理消息 | 批量删除消息 |
| `!kick @用户` | 踢人 | 踢出用户 |
| `!ban @用户` | 封禁 | 封禁用户 |

## 🛠️ 定制化

### 添加新命令
在 `bot/handlers.py` 中添加：

```python
class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="hello")
    async def hello(self, ctx):
        await ctx.send(f"Hello {ctx.author.mention}!")
```

然后在 `bot/__main__.py` 的 `setup_hook` 中加载。

### 换用其他 AI 模型
修改 `bot/ai.py`，支持 Claude、本地 Ollama 等。

## 📁 项目结构

```
discord-bot/
├── bot/
│   ├── __init__.py    # 版本信息
│   ├── __main__.py    # 入口 + Bot 类
│   ├── config.py      # 配置管理
│   ├── ai.py          # AI 对话模块
│   └── handlers.py    # 事件 & 命令
├── .env.example       # 配置模板
├── requirements.txt   # Python 依赖
├── Dockerfile         # Docker 镜像
├── docker-compose.yml # Docker Compose
└── README.md          # 本文档
```

## 📄 许可证

MIT — 可自由用于商业项目。

---

**需要定制？** 联系我获取专业开发服务。
