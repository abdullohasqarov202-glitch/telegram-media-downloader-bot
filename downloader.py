import yt_dlp
import uuid


def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True,

        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)
            return file
    except Exception as e:
        print(e)
        return None


def download_audio(url):

    filename = f"audio_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)
            return file
    except Exception as e:
        print(e)
        return None
