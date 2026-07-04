#!/usr/bin/env python3
"""
网页采集脚本 — 简单版
客户只需改下面几个参数就能用
"""
import argparse
import json
import sys
from datetime import datetime
from urllib.request import Request, urlopen

from bs4 import BeautifulSoup

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


def scrape(url: str, selector: str, attr: str = "text") -> dict:
    """采集网页内容"""
    req = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(req, timeout=30) as resp:
        html = resp.read().decode("utf-8", errors="replace")

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string.strip() if soup.title else ""

    elements = soup.select(selector)
    if attr in ("text", "inner_text"):
        results = [el.get_text().strip() for el in elements]
    elif attr == "html":
        results = [str(el) for el in elements]
    else:
        results = [el.get(attr, "") for el in elements]

    return {
        "url": url,
        "title": title,
        "count": len(results),
        "results": results,
        "timestamp": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="网页采集工具")
    parser.add_argument("url", help="目标网址")
    parser.add_argument("-s", "--selector", default="h1", help="CSS 选择器 (默认: h1)")
    parser.add_argument("-a", "--attr", default="text", help="提取属性: text/html/href/src (默认: text)")
    parser.add_argument("-o", "--output", help="输出 JSON 文件路径")
    args = parser.parse_args()

    try:
        result = scrape(args.url, args.selector, args.attr)
    except Exception as e:
        print(f"❌ 采集失败: {e}", file=sys.stderr)
        sys.exit(1)

    output = json.dumps(result, ensure_ascii=False, indent=2)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
        print(f"✅ 结果已保存到 {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
