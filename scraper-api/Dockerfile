FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 安装 Playwright 浏览器（用于 JS 渲染采集）
RUN pip install --no-cache-dir playwright && \
    playwright install --with-deps chromium && \
    playwright install-deps chromium

# 复制源码
COPY scraper/ ./scraper/

# 数据目录
RUN mkdir -p /app/data

EXPOSE 8000

CMD ["uvicorn", "scraper.main:app", "--host", "0.0.0.0", "--port", "8000"]
