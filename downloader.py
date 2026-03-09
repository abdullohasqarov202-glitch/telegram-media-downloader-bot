import yt_dlp


def download_video(url):

    ydl_opts = {
        "format": "bestvideo+bestaudio/best",
        "outtmpl": "video.%(ext)s",
        "merge_output_format": "mp4",
        "noplaylist": True,
        "quiet": True,
        "nocheckcertificate": True,

        # YouTube blok bo'lmasligi uchun
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
        "format": "bestaudio/best",
        "outtmpl": "audio.%(ext)s",
        "quiet": True,

        # MP3 ga o‘tkazish
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return "audio.mp3"
    except Exception as e:
        print(e)
        return None
