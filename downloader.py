import yt_dlp
import uuid

def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bv*[ext=mp4]+ba/b[ext=mp4]/best",
        "outtmpl": filename,
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True,
        "ignoreerrors": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                return None

            file = ydl.prepare_filename(info)
            return file

    except Exception as e:
        print(e)
        return None


def download_audio(url):

    filename = f"audio_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                return None

            file = ydl.prepare_filename(info)
            return file

    except Exception as e:
        print(e)
        return None
