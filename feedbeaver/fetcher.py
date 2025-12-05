import yt_dlp
import os


def download_video(entry, feed):
    download_path = feed["download_path"]
    filename_template = feed["filename_template"]
    cookie_file = feed["cookie_file"]

    os.makedirs(download_path, exist_ok=True)

    # 允许 feed 专属的 yt-dlp 配置（可选）
    extra_opts = feed.get("ytdlp", {})

    ydl_opts = {
        "outtmpl": os.path.join(download_path, filename_template),
        "cookiefile": cookie_file,
        "ignoreerrors": True,
        "no_warnings": True,
        "quiet": False,
        **extra_opts
    }

    url = entry.get("link")

    print(f"[FeedBeaver] Downloading: {entry.get('title')}")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print(f"[FeedBeaver] Download complete.")
    except Exception as e:
        print(f"[FeedBeaver] Download failed: {e}")