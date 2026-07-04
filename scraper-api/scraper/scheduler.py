"""
定时调度器 — 简单 APScheduler 封装
"""

import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

log = logging.getLogger("scraper.scheduler")


class Scheduler:
    """任务调度器"""

    def __init__(self):
        self._scheduler = AsyncIOScheduler()
        self._tasks: dict[str, str] = {}  # job_id -> apscheduler job_id

    async def start(self):
        self._scheduler.start()
        log.info("⏰ 调度器已启动")

    async def stop(self):
        self._scheduler.shutdown(wait=False)
        log.info("⏰ 调度器已停止")

    def add_cron(self, job_id: str, cron_expr: str, func, **kwargs):
        """添加 cron 定时任务"""
        trigger = CronTrigger.from_crontab(cron_expr)
        aps_job = self._scheduler.add_job(
            func,
            trigger=trigger,
            id=job_id,
            kwargs=kwargs,
            replace_existing=True,
        )
        self._tasks[job_id] = aps_job.id
        log.info(f"📅 已添加定时任务: {job_id} ({cron_expr})")

    def remove(self, job_id: str):
        """移除定时任务"""
        if job_id in self._tasks:
            self._scheduler.remove_job(self._tasks[job_id])
            del self._tasks[job_id]
            log.info(f"🗑️ 已移除定时任务: {job_id}")


# 全局调度器实例
scheduler = Scheduler()
