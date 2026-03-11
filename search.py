import yt_dlp

def search_song(query):

    ydl_opts = {
        "quiet": True,
        "default_search": "ytsearch5"
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:

        info = ydl.extract_info(query, download=False)

        results = []

        if "entries" not in info:
            return results

        for v in info["entries"]:

            results.append({
                "title": v["title"],
                "url": v["webpage_url"]
            })

        return results
