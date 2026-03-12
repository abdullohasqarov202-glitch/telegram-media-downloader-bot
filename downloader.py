import yt_dlp

def download_video(url):
    ydl_opts = {
        "format": "bv*+ba/b",
        "outtmpl": "video.%(ext)s",
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return "audio.mp3"


def download_audio(url):

    filename = f"audio_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,
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
