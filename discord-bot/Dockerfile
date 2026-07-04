# Discord Bot SaaS Template
FROM python:3.11-slim

WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY bot/ ./bot/

# 运行
CMD ["python", "-m", "bot"]
