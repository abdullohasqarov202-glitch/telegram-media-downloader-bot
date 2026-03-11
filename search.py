import yt_dlp


def search_song(query):

    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch1"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(query, download=False)

        video = info["entries"][0]

        return video["webpage_url"], video["title"]
