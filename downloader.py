import yt_dlp
import uuid

def download_video(url):

    filename = f"video_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bv*+ba/b",
        "outtmpl": filename,
        "merge_output_format": "mp4"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def download_audio(url):

    filename = f"audio_{uuid.uuid4().hex}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.extract_info(url, download=True)

    return filename.replace("%(ext)s", "mp3")
