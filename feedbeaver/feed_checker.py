import time
import feedparser
from pathlib import Path
from fetcher import download_video
import json


STATE_FILE = Path(__file__).resolve().parent / "data" / "state.json"


def load_state():
    if not STATE_FILE.exists():
        return {}
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return {}


def save_state(state):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def check_feed(feed, state):
    """单次检查单个 feed"""
    print(f"[FeedBeaver] Checking: {feed['name']}")

    parsed = feedparser.parse(feed["url"])
    if not parsed.entries:
        print(f"[FeedBeaver] No entries found: {feed['name']}")
        return

    for entry in parsed.entries:
        video_id = entry.get("id") or entry.get("link")

        if not video_id:
            continue

        # 跳过已下载的逻辑（支持全局 + 单 feed）
        if feed.get("skip_downloaded", True) and video_id in state:
            continue

        # 下载视频
        download_video(entry, feed)

        # 记录状态
        state[video_id] = True
        save_state(state)


def monitor_feeds(config):
    """循环监控所有 feed，支持独立 check_interval"""

    feeds = config["feeds"]
    state = load_state()

    # 每个 feed 单独记录上次检查时间
    last_check = {feed["url"]: 0 for feed in feeds}

    while True:
        now = time.time()

        for feed in feeds:
            interval = feed["check_interval"]

            if now - last_check[feed["url"]] >= interval:
                check_feed(feed, state)
                last_check[feed["url"]] = now

        time.sleep(2)