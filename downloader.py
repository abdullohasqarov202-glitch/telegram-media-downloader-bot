import yt_dlp
import uuid


def fix_url(url):

    if "youtube.com/shorts/" in url:
        video_id = url.split("shorts/")[1].split("?")[0]
        return f"https://www.youtube.com/watch?v={video_id}"

    return url


def download_video(url):

    url = fix_url(url)

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
                "player_client": ["android", "web"]
            }
        },

        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename


def download_audio(url):

    url = fix_url(url)

    filename = f"{uuid.uuid4().hex}.mp3"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,
        "ffmpeg_location": "/usr/bin/ffmpeg",

        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename
