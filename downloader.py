import yt_dlp

def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'ffmpeg_location': '/usr/bin/ffmpeg'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


def download_audio(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'ffmpeg_location': '/usr/bin/ffmpeg',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)

    return "audio.mp3"
