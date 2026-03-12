import yt_dlp
import uuid


def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.mp4"

    ydl_opts = {
        "outtmpl": filename,
        "format": "best",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename


def download_audio(url):

    filename = f"audio_{uuid.uuid4().hex}.mp3"

    ydl_opts = {
        "outtmpl": filename,
        "format": "bestaudio",
        "noplaylist": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return filename
