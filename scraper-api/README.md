# 🕷️ Web Scraper API — 智能网页采集服务

**FastAPI 驱动的网页采集服务**，支持定时采集、CSS/XPath 提取、浏览器渲染。RESTful JSON API，客户即接即用。

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 🔍 智能采集 | CSS 选择器 / XPath 双重支持 |
| 🖥️ 浏览器渲染 | Playwright 驱动，JS 动态页面无障碍 |
| ⏰ 定时任务 | Cron 表达式定时采集，数据自动入库 |
| 📊 结果缓存 | 自动保留最近 50 条采集记录 |
| 🔌 RESTful API | Swagger 文档 (/docs)，客户自行对接 |
| 🐳 Docker 部署 | 一条命令上线 |

## 🚀 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置
cp .env.example .env

# 3. 启动服务
uvicorn scraper.main:app --reload --port 8000

# 4. 打开 Swagger 文档
# http://localhost:8000/docs
```

### Docker 部署

```bash
docker compose up -d
```

## 📡 API 接口

### 立即采集

```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com",
    "selector": "h1",
    "selector_type": "css",
    "attribute": "text"
  }'
```

### 定时采集

```bash
curl -X POST http://localhost:8000/api/v1/scrape \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/news",
    "selector": ".article-title",
    "schedule": "0 */6 * * *"
  }'
```

### 查看结果

```bash
curl http://localhost:8000/api/v1/scrape/<job_id>
```

### 端点一览

| 方法 | 路径 | 说明 |
|------|------|------|
| `GET` | `/` | 服务信息 |
| `GET` | `/docs` | Swagger 文档 |
| `GET` | `/api/v1/health` | 健康检查 |
| `POST` | `/api/v1/scrape` | 提交采集任务 |
| `GET` | `/api/v1/scrape/{id}` | 查看采集结果 |
| `GET` | `/api/v1/jobs` | 列出定时任务 |
| `DELETE` | `/api/v1/jobs/{id}` | 删除定时任务 |

## 🛠️ 技术栈

`Python 3.11` · `FastAPI` · `BeautifulSoup4` · `Playwright` · `APScheduler` · `Docker`

## 💰 定制服务

需要定制功能？支持但不限于：

- 电商平台专项采集（淘宝/京东/拼多多）
- 验证码 / 反爬对抗
- 数据清洗 + 导出 Excel
- 钉钉/飞书/企业微信通知
- 分布式采集集群

📧 联系：1653526777@QQ.com
