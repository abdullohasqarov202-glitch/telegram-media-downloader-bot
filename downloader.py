import yt_dlp

def download_video(url):

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "video.%(ext)s",
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True
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
        "format": "bestaudio/best",
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
