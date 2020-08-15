from urllib.parse import quote
from urllib.request import urlopen
from bs4 import BeautifulSoup as bs
from youtube import get_youtube_manager
from threading import Thread
from text_to_speech import play_song
from text_to_speech import play_sound
from text_to_speech import read_text
from pytube import YouTube
import time
from requests_html import HTMLSession

# Read 3 first top song, cuz download take long time
def message(videos):
    msg = "I found " + str(len(videos)) + " songs, "
    for index, video in enumerate(videos):
        msg = msg + "The number " + str(index + 1) + " song is " + video["title"] + ", "
        if (index == 3): break
    return msg

def web_parsing(textToSearch):
    print('a')
    try:
        query = quote(textToSearch)
        session = HTMLSession()
        url = "https://www.youtube.com/results?search_query=" + query
        response = session.get(url)
        response.html.render(sleep=1)
        soup = bs(response.html.html, 'html.parser')
        read_text("Searching for " + textToSearch)
        tempYoutube = "https://www.youtube.com"
        linkHref = soup.find(id="video-title").get('href')
        print(len(linkHref))
        if len(linkHref)>0:
            youtubeHref = tempYoutube + linkHref;
            ydl = get_youtube_manager()
            Thread(target=web_parsing, args=[youtubeHref]).start()
            ydl.download([youtubeHref])
            play_sound('./musics/song.mp3')

    except Exception as e:
        print(e)

# web_parsing("Solo")
# play_song("./musics/Owl City - Fireflies-psuRGfAaju4.mp3")