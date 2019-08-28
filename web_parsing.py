from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup
from youtube import get_youtube_manager
import os
from threading import Thread
from text_to_speech import play_song
from text_to_speech import read_text


# # Delete all old music
# def remove_old_musics(mydir):
#     filelist = os.listdir(mydir)
#     for f in filelist:
#         os.remove(os.path.join(mydir, f))


# Read 3 first top song, cuz download take long time
def message(videos):
    msg = "I found " + str(len(videos)) + " songs, "
    for index, video in enumerate(videos):
        msg = msg + "The number " + str(index + 1) + " song is " + video["title"] + ", "
        if (index == 3): break
    return msg


def web_parsing(textToSearch):
    #remove_old_musics("musics")
    query = quote(textToSearch)
    url = "https://www.youtube.com/results?search_query=" + query
    response = urlopen(url)
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    read_text("Searching for " + textToSearch)
    videos = soup.findAll(attrs={'class': 'yt-uix-tile-link'})
    if len(videos):
        video = videos[0]
        print('https://www.youtube.com' + video['href'])
        ydl = get_youtube_manager()

        Thread(target=read_text, args=[message(videos)]).start()

        ydl.download(['https://www.youtube.com' + video['href']])

        play_song('./musics/song.mp3')


# web_parsing("Solo")
# play_song("./musics/Owl City - Fireflies-psuRGfAaju4.mp3")

