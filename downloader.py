import yt_dlp
import uuid


def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "best",
        "outtmpl": filename,
        "quiet": True,
        "noplaylist": True
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

    filename = "audio.%(ext)s"

    ydl_opts = {
        "format": "bestaudio",
        "outtmpl": filename,
        "quiet": True,
        "ffmpeg_location": "/usr/bin/ffmpeg",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return "audio.mp3"
    except Exception as e:
        print(e)
        return None
