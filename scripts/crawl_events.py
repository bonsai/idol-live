#!/usr/bin/env python3
"""Fetch candidate event pages and build normalized idol-live data.

The workflow is the driver; this file contains executable crawling/normalization code.
Design decisions live in GitHub Issues, not in this source file.
"""
from __future__ import annotations

import html
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / ".data"
EVENTS = DATA / "events.json"
AUX = DATA / "auxiliary.json"

INCLUDE = ("アイドル", "idol", "ライブ", "live", "フリーライブ", "無銭", "観覧無料")
EXHIBITION = ("展示会", "展覧会", "美術展", "写真展", "作品展示", "exhibition", "museum")
FREE = ("無料", "0円", "￥0", "¥0", "フリーライブ", "無銭", "観覧無料")


def fetch(url: str) -> str:
    req = Request(url, headers={"User-Agent": "bonsai-idol-live/1.0"})
    with urlopen(req, timeout=20) as response:
        return response.read().decode("utf-8", errors="replace")


def text_from_html(source: str) -> str:
    source = re.sub(r"<script\b[^>]*>.*?</script>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<style\b[^>]*>.*?</style>", " ", source, flags=re.I | re.S)
    source = re.sub(r"<[^>]+>", " ", source)
    return re.sub(r"\s+", " ", html.unescape(source)).strip()


def classify(text: str) -> str:
    lower = text.lower()
    idol_score = sum(term.lower() in lower for term in INCLUDE)
    exhibition_score = sum(term.lower() in lower for term in EXHIBITION)
    if exhibition_score >= 2 and idol_score < 3:
        return "exhibition"
    if idol_score >= 2:
        return "idol_live"
    return "nearby"


def normalize(text: str, url: str, fetched_at: str) -> dict:
    lower = text.lower()
    free = any(term.lower() in lower for term in FREE)
    drink = bool(re.search(r"1\s*[dD]|ドリンク", text))
    reservation = bool(re.search(r"予約|要予約|予約必須", text))
    date_match = re.search(r"20\d{2}[/-]\d{1,2}[/-]\d{1,2}", text)
    return {
        "date": date_match.group(0).replace("/", "-") if date_match else None,
        "title": text[:160],
        "admission": {"price": 0 if free else None, "free": free, "drink_required": drink, "reservation_required": reservation},
        "source_url": url,
        "fetched_at": fetched_at,
    }


def main() -> int:
    DATA.mkdir(exist_ok=True)
    now = datetime.now(timezone.utc).isoformat()
    existing = json.loads(EVENTS.read_text(encoding="utf-8")) if EVENTS.exists() else {"dataset": "idol_free_live", "events": []}
    auxiliary = {"dataset": "idol_free_live_auxiliary", "generated_at": now, "candidates": []}

    sources = []
    sources_file = DATA / "sources.json"
    if sources_file.exists():
        sources = json.loads(sources_file.read_text(encoding="utf-8")).get("sources", [])

    for source in sources:
        url = source.get("url")
        if not url:
            continue
        try:
            body = fetch(url)
            text = text_from_html(body)
            kind = classify(text)
            item = normalize(text, url, now)
            if kind == "idol_live":
                existing.setdefault("events", []).append(item)
            elif kind == "nearby":
                item["reason"] = "low-confidence-or-related"
                auxiliary["candidates"].append(item)
            # Exhibition candidates are deliberately not written to the primary dataset.
        except Exception as exc:  # keep one bad source from aborting the crawl
            auxiliary["candidates"].append({"source_url": url, "error": str(exc), "fetched_at": now})

    dedup = {}
    for event in existing.get("events", []):
        key = (event.get("date"), event.get("source_url"), event.get("title"))
        dedup[str(key)] = event
    existing["events"] = list(dedup.values())
    EVENTS.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    AUX.write_text(json.dumps(auxiliary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
