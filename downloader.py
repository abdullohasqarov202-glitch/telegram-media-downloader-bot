import yt_dlp
import uuid


def download_video(url):

    filename = f"{uuid.uuid4().hex}.mp4"

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,
        "quiet": True,
        "http_headers": {
            "User-Agent": "Mozilla/5.0"
        },
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        }
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename


def download_audio(url):

    filename = f"{uuid.uuid4().hex}.mp3"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,
        "quiet": True,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename
