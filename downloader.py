import yt_dlp
import uuid


def download_video(url):

    filename = f"{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,

        "quiet": True,
        "noplaylist": True,

        "cookiefile": "cookies.txt",

        "http_headers": {
            "User-Agent": "Mozilla/5.0 (Linux; Android 10)"
        },

        "extractor_args": {
            "youtube": {
                "player_client": ["web"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        file = ydl.prepare_filename(info)

    return file


def download_audio(url):

    filename = f"{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,

        "quiet": True,
        "noplaylist": True,

        "cookiefile": "cookies.txt",

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        file = ydl.prepare_filename(info)

    return file.replace(".webm",".mp3").replace(".m4a",".mp3")
