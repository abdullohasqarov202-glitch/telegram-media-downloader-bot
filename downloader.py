import yt_dlp
import uuid


# VIDEO YUKLASH
def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "merge_output_format": "mp4"
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


# MP3 YUKLASH
def download_audio(query):

    filename = f"audio_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192"
            }
        ]
    }

    try:

        url = f"ytsearch1:{query}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            if not info:
                return None

            info = info["entries"][0]

            file = ydl.prepare_filename(info)

            return file.rsplit(".", 1)[0] + ".mp3"

    except Exception as e:
        print(e)
        return None
