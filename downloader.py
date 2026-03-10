import yt_dlp
import uuid

def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,
        "noplaylist": True,
        "quiet": True,

        "cookiefile": "cookies.txt",

        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        }
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
