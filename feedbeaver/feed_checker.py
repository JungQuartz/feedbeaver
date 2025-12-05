import feedparser
import json
import os


STATE_FILE = "states.json"


def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)


def check_rss_list(rss_list, state):
    new_videos = []

    for rss_url in rss_list:
        feed = feedparser.parse(rss_url)
        if not feed.entries:
            continue

        latest_id = state.get(rss_url)
        entries = feed.entries

        # 遇到已下载记录就停止（RSS按时间倒序）
        for entry in entries:
            if entry.get("id") == latest_id:
                break
            new_videos.append({
                "id": entry.get("id"),
                "title": entry.get("title"),
                "link": entry.get("link"),
                "published": entry.get("published"),
                "rss": rss_url
            })

        # 更新最新 id
        state[rss_url] = entries[0].get("id")

    return new_videos, state