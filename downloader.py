import yt_dlp
import uuid


def download_video(url):

    filename = f"{uuid.uuid4().hex}.mp4"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,

        "cookiefile": "cookies.txt",

        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        },

        "geo_bypass": True,
        "nocheckcertificate": True,

        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "web"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename


def download_audio(url):

    filename = f"{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,

        "cookiefile": "cookies.txt",

        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        },

        "geo_bypass": True,
        "nocheckcertificate": True,

        "extractor_args": {
            "youtube": {
                "player_client": ["android", "ios", "web"]
            }
        },

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        file = ydl.prepare_filename(info)

    return file.replace(".webm", ".mp3").replace(".m4a", ".mp3")
