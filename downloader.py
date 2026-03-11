import yt_dlp
import uuid


# VIDEO YUKLASH (SIFAT BILAN)
def download_video(url, quality="720"):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": f"bestvideo[height<={quality}]+bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,
        "nocheckcertificate": True,
        "ignoreerrors": True,
        "merge_output_format": "mp4",

        "extractor_args": {
            "youtube": {
                "player_client": ["android"]
            }
        }
    }

    try:

        # agar link bo'lmasa qo'shiq qidiradi
        if not url.startswith("http"):
            url = f"ytsearch1:{url}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            if not info:
                return None

            # search bo'lsa
            if "entries" in info:
                info = info["entries"][0]

            return ydl.prepare_filename(info)

    except Exception as e:
        print(e)
        return None


# MP3 YUKLASH
def download_audio(url):

    filename = f"audio_{uuid.uuid4().hex}.mp3"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True,

        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]
    }

    try:

        if not url.startswith("http"):
            url = f"ytsearch1:{url}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:

            info = ydl.extract_info(url, download=True)

            if not info:
                return None

            if "entries" in info:
                info = info["entries"][0]

            return filename

    except Exception as e:
        print(e)
        return None
