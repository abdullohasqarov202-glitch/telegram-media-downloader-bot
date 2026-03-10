import yt_dlp
import uuid


def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": filename,
        "noplaylist": True,
        "quiet": True,

        # YouTube blokni chetlab o'tish
        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },

        # Cookie ishlatish
        "cookiefile": "cookies.txt",

        # Server muammolari uchun
        "nocheckcertificate": True,
        "ignoreerrors": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                return None

            return ydl.prepare_filename(info)

    except Exception as e:
        print(e)
        return None


def download_audio(url):

    filename = f"audio_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,

        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        },

        "cookiefile": "cookies.txt"
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)

            if not info:
                return None

            return ydl.prepare_filename(info)

    except Exception as e:
        print(e)
        return None
