import wikipedia
from text_to_speech import read_text
import bs4
import requests
import re

def format_search_text(text):
    return text.strip().capitalize().replace(' ', '_');

# Search wikipedia function
def search_wikipedia(text):
    url = "https://vi.wikipedia.org/wiki/"
    urlNew = url + format_search_text(text)
    print(urlNew)
    response = requests.get(urlNew)
    if response is not None:
        page = bs4.BeautifulSoup(response.text, 'html.parser')
        title = page.select("#firstHeading")[0].text
        wikipedia.set_lang("vi")
        print(wikipedia.summary(title))
        if wikipedia.summary(title):
            read_text('Theo Wikipedia')
            str = wikipedia.summary(title)
            # Paragraph with 2 sentences
            para = '.'.join(re.split('\.(?=\s*[A-Z])', str)[:2]) + '.'
            # Remove Parentheses
            info = re.sub("[\(\[].*?[\)\]]", "", para)
            read_text(info)

# search_wikipedia('khủng long')
