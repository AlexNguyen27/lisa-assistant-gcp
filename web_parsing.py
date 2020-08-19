from urllib.parse import quote
from youtube import get_youtube_manager
from text_to_speech import  play_song
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def message(videos):
    msg = "I found " + str(len(videos)) + " songs, "
    for index, video in enumerate(videos):
        msg = msg + "The number " + str(index + 1) + " song is " + video["title"] + ", "
        if (index == 3): break

def web_parsing(textToSearch):
    try:
        query = quote(textToSearch)
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://www.youtube.com/results?search_query="+query)
        videos = driver.find_elements_by_xpath('//*[@id="video-title"]')
        read_text("Searching for " + textToSearch)
        if len(videos):
            linkHref = videos[0].get_attribute('href')
            driver.quit()
            ydl = get_youtube_manager()
            ydl.download([linkHref])
            play_song('./musics/song.mp3')
    except Exception as e:
        print(e)

# web_parsing("Solo")
# play_song("./musics/Owl City - Fireflies-psuRGfAaju4.mp3")
# listBLE()
