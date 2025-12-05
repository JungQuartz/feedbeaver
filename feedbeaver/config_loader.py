from pathlib import Path
import yaml


def deep_merge(a, b):
    """b 覆盖 a，生成新 dict"""
    result = a.copy()
    for key, value in b.items():
        if isinstance(value, dict) and key in result:
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result


def load_config():
    base_dir = Path(__file__).resolve().parent
    config_path = base_dir / "config" / "config.yaml"

    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")

    config = yaml.safe_load(config_path.read_text(encoding="utf-8"))

    global_config = config.get("global", {})
    feeds = config.get("feeds", [])

    # 合并 global + feed 覆盖
    merged_feeds = []
    for feed in feeds:
        merged_feeds.append(deep_merge(global_config, feed))

    return {
        "global": global_config,
        "feeds": merged_feeds
    }