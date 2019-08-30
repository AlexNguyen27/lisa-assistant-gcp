import wikipedia
from text_to_speech import read_text
import bs4
import requests
import re


# Search wikipedia function
def search_wikipedia(text):
    url = "https://en.wikipedia.org/wiki/"
    urlNew = url + text
    print(urlNew)
    response = requests.get(urlNew)
    if response is not None:
        page = bs4.BeautifulSoup(response.text, 'html.parser')
        read_text('Searching for ' + text)
        title = page.select("#firstHeading")[0].text
        if wikipedia.summary(title):
            read_text('According to Wikipedia' + title)
            str = wikipedia.summary(title)
            # Paragraph with 2 sentences
            para = '.'.join(re.split('\.(?=\s*[A-Z])', str)[:2]) + '.'
            # Remove Parentheses
            info = re.sub("[\(\[].*?[\)\]]", "", para)
            read_text(info)

# search_wikipedia('lisa')
