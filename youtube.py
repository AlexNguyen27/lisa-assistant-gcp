import youtube_dl

ydl_opts = {
    'outtmpl': 'musics/%(title)s-%(id)s.%(ext)s',
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192'
    }],
}


def get_youtube_manager():
    return youtube_dl.YoutubeDL(ydl_opts)

# ydl = get_youtube_manager()
