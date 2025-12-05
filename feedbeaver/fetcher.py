import yt_dlp
import os


def download_video(video, config):
    download_path = config["download_path"]
    filename_template = config["filename_template"]
    cookie_file = config.get("cookie_file", None)

    # 基础参数
    ydl_opts = {
        "outtmpl": os.path.join(download_path, filename_template),
        "quiet": False,
    }

    # cookie 支持
    if cookie_file and os.path.exists(cookie_file):
        ydl_opts["cookiefile"] = cookie_file

    # 合并 config.yaml 中的 yt_dlp_options
    if "yt_dlp_options" in config:
        for key, value in config["yt_dlp_options"].items():
            ydl_opts[key] = value

    # 如果希望自动跳过已下载
    if config.get("skip_downloaded", True):
        ydl_opts["download_archive"] = os.path.join(download_path, "downloaded.txt")

    os.makedirs(download_path, exist_ok=True)

    print(f"开始下载: {video['title']}  ({video['link']})")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video["link"]])