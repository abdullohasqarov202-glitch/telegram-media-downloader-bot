import yt_dlp

def download_video(url):

    ydl_opts = {
        "format": "best[ext=mp4]/best",
        "outtmpl": "video.%(ext)s",
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

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": "audio.%(ext)s",
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file = ydl.prepare_filename(info)
            return file
    except Exception as e:
        print(e)
        return None
