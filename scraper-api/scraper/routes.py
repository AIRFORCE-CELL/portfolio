"""
API 路由 — 采集任务 CRUD + 执行
"""

import hashlib
import json
import logging
import time
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from scraper.config import settings
from scraper.scheduler import scheduler

router = APIRouter()
log = logging.getLogger("scraper.routes")

# ── 简单的内存存储（生产环境换数据库） ──────────
_jobs: dict[str, dict] = {}
_results: dict[str, list[dict]] = {}


# ── Models ────────────────────────────────────────

class ScrapeRequest(BaseModel):
    url: str = Field(..., description="目标 URL")
    selector: Optional[str] = Field(None, description="CSS 选择器")
    selector_type: str = Field("css", description="css | xpath")
    attribute: Optional[str] = Field(None, description="提取属性 (text/html/src/href)")
    use_browser: bool = Field(False, description="是否使用浏览器渲染")
    schedule: Optional[str] = Field(
        None, description="定时采集 cron 表达式"
    )
    tags: list[str] = Field(default_factory=list)


class ScrapeResponse(BaseModel):
    job_id: str
    status: str
    result: Optional[dict] = None
    error: Optional[str] = None
    duration_ms: int = 0


# ── Routes ────────────────────────────────────────

@router.get("/health")
async def health():
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


@router.post("/scrape", response_model=ScrapeResponse)
async def scrape(req: ScrapeRequest):
    """立即执行采集任务"""
    job_id = _make_job_id(req.url, req.selector or "")

    start = time.time()
    try:
        result = await _do_scrape(req)
        duration = int((time.time() - start) * 1000)

        # 存储结果
        if job_id not in _results:
            _results[job_id] = []
        _results[job_id].append(
            {"timestamp": datetime.now().isoformat(), "data": result}
        )
        _results[job_id] = _results[job_id][-50:]  # 保留最近 50 条

        # 设置定时任务
        if req.schedule:
            _jobs[job_id] = {
                "url": req.url,
                "selector": req.selector,
                "schedule": req.schedule,
                "tags": req.tags,
                "created": datetime.now().isoformat(),
            }

        return ScrapeResponse(
            job_id=job_id,
            status="success",
            result=result,
            duration_ms=duration,
        )
    except Exception as e:
        duration = int((time.time() - start) * 1000)
        log.error(f"采集失败 {req.url}: {e}")
        return ScrapeResponse(
            job_id=job_id,
            status="error",
            error=str(e),
            duration_ms=duration,
        )


@router.get("/scrape/{job_id}")
async def get_results(job_id: str):
    """获取采集结果"""
    results = _results.get(job_id, [])
    return {"job_id": job_id, "count": len(results), "results": results}


@router.get("/jobs")
async def list_jobs():
    """列出所有定时任务"""
    return {"jobs": list(_jobs.values())}


@router.delete("/jobs/{job_id}")
async def delete_job(job_id: str):
    """删除定时任务"""
    _jobs.pop(job_id, None)
    _results.pop(job_id, None)
    return {"status": "deleted"}


# ── Core ──────────────────────────────────────────

async def _do_scrape(req: ScrapeRequest) -> dict:
    """执行采集"""
    import re

    import aiohttp
    from bs4 import BeautifulSoup

    headers = {"User-Agent": settings.user_agent}

    # 浏览器渲染
    if req.use_browser and settings.use_browser:
        return await _scrape_with_browser(req)

    # HTTP 采集
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(
            req.url, timeout=aiohttp.ClientTimeout(total=settings.default_timeout)
        ) as resp:
            resp.raise_for_status()
            html = await resp.text()

    soup = BeautifulSoup(html, "html.parser")

    # 提取标题
    title = soup.title.string.strip() if soup.title else ""

    # 提取元描述
    meta_desc = ""
    meta_tag = soup.find("meta", attrs={"name": "description"})
    if meta_tag:
        meta_desc = meta_tag.get("content", "")

    # CSS 选择器提取
    extracted = []
    if req.selector:
        if req.selector_type == "xpath":
            # BeautifulSoup 不直接支持 XPath，用 lxml
            try:
                from lxml import html as lhtml

                tree = lhtml.fromstring(html)
                elements = tree.xpath(req.selector)
                extracted = [_extract_element(el, req.attribute) for el in elements]
            except ImportError:
                raise HTTPException(
                    400, "XPath 需要安装 lxml: pip install lxml"
                )
        else:
            elements = soup.select(req.selector)
            extracted = [_extract_element(el, req.attribute) for el in elements]

    # 统计
    word_count = len(soup.get_text().split())

    return {
        "url": req.url,
        "title": title,
        "meta_description": meta_desc,
        "word_count": word_count,
        "extracted_count": len(extracted),
        "extracted": extracted[:100],  # 最多返回 100 条
        "timestamp": datetime.now().isoformat(),
    }


async def _scrape_with_browser(req: ScrapeRequest) -> dict:
    """使用 Playwright 浏览器渲染采集"""
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise HTTPException(400, "浏览器渲染需要安装 playwright: pip install playwright && playwright install")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=settings.headless)
        page = await browser.new_page()
        await page.goto(req.url, timeout=settings.default_timeout * 1000)

        title = await page.title()

        extracted = []
        if req.selector:
            elements = await page.query_selector_all(req.selector)
            for el in elements:
                if req.attribute in (None, "text"):
                    text = await el.inner_text()
                    extracted.append(text.strip())
                else:
                    attr = await el.get_attribute(req.attribute)
                    extracted.append(attr)

        await browser.close()

        return {
            "url": req.url,
            "title": title,
            "extracted_count": len(extracted),
            "extracted": extracted[:100],
            "method": "browser",
            "timestamp": datetime.now().isoformat(),
        }


def _extract_element(el, attribute: Optional[str] = None) -> str:
    """从元素提取内容"""
    if attribute is None or attribute in ("text", "inner_text"):
        return el.get_text().strip()
    elif attribute == "html":
        return str(el)
    else:
        return el.get(attribute, "")


def _make_job_id(url: str, selector: str) -> str:
    raw = f"{url}|{selector}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]
