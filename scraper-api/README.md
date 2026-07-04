# 🕷️ Web Scraper API Service

FastAPI 驱动的智能网页采集服务。支持 CSS/XPath 选择器、定时采集、浏览器渲染。

## ✨ 功能

- ✅ **RESTful API** — POST 下发任务，GET 获取结果
- ✅ **CSS / XPath** — 支持两种选择器提取数据
- ✅ **定时采集** — Cron 表达式，自动周期执行
- ✅ **浏览器渲染** — 可选 Playwright，采集 SPA 页面
- ✅ **自动摘要** — 自动提取标题、描述、字数统计
- ✅ **Swagger 文档** — 访问 `/docs` 即可交互测试
- ✅ **Docker 部署** — 含完整 Dockerfile + docker-compose

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. (可选) 安装浏览器渲染
# pip install playwright && playwright install chromium

# 3. 配置
cp .env.example .env

# 4. 启动
uvicorn scraper.main:app --reload

# 5. 打开文档
# http://localhost:8000/docs
```

**Docker:**
```bash
docker-compose up -d
```

## 📡 API 使用

### 立即采集
```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://news.ycombinator.com",
    "selector": ".titleline > a",
    "attribute": "text"
  }'
```

### 定时采集（每 30 分钟）
```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/price",
    "selector": ".price",
    "schedule": "*/30 * * * *",
    "tags": ["price-monitor"]
  }'
```

### 获取结果
```bash
curl http://localhost:8000/api/v1/scrape/{job_id}
```

## 🛠️ 典型用例

| 场景 | 说明 |
|------|------|
| 电商竞品监控 | 定时采集对手价格、库存 |
| 舆情分析 | 采集社媒/论坛指定话题 |
| 数据聚合 | 多源数据采集 + 汇总输出 |
| 内容监控 | 监测页面变化、新内容通知 |

## 📁 项目结构

```
scraper-api/
├── scraper/
│   ├── __init__.py    # 版本
│   ├── main.py        # FastAPI 应用入口
│   ├── config.py      # 配置管理
│   ├── routes.py      # API 路由 + 采集引擎
│   └── scheduler.py   # 定时调度器
├── .env.example
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── README.md
```

## 📄 许可证

MIT — 可自由商用。
