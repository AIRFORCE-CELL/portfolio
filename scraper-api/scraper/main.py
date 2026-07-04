"""
FastAPI 主应用
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scraper.config import Settings
from scraper.routes import router
from scraper.scheduler import Scheduler

log = logging.getLogger("scraper")

# ── 生命周期 ────────────────────────────────────

scheduler = Scheduler()


@asynccontextmanager
async def lifespan(app: FastAPI):
    log.info("🚀 采集服务启动")
    await scheduler.start()
    yield
    await scheduler.stop()
    log.info("👋 采集服务关闭")


# ── App ─────────────────────────────────────────

settings = Settings()

app = FastAPI(
    title="Web Scraper API",
    description="智能网页采集服务 — 支持定时采集、CSS选择器、JSON输出",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "service": "Web Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
