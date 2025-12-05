import time
import yaml
from feed_checker import check_rss_list, load_state, save_state
from fetcher import download_video
from pathlib import Path


def main():

    config = load_config()

    rss_list = config["rss_list"]
    check_interval = config["check_interval"]

    print("feedbeaver服务启动...")

    # 读取已记录状态
    state = load_state()

    while True:
        print("\n=== 开始检查 RSS 更新 ===")

        new_videos, new_state = check_rss_list(rss_list, state)

        if new_videos:
            print(f"发现 {len(new_videos)} 个新视频，准备下载...")
            for video in new_videos:
                download_video(video, config)
        else:
            print("无更新")

        save_state(new_state)
        state = new_state

        print(f"等待 {check_interval} 秒后再次检查...\n")
        time.sleep(check_interval)

def load_config():
    base_dir = Path(__file__).resolve().parent  # feedbeaver/
    config_path = base_dir / "config" / "config.yaml"

    with config_path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)

if __name__ == "__main__":
    main()