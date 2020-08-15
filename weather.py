import requests
from text_to_speech import read_text

# Searching for weather
def weather():
    url = 'https://api.openweathermap.org/data/2.5/weather?id=1566083&appid=a395d3d89b3fc57be94693534c103fe4'
    payload = {}
    headers = {}
    res = requests.request("GET", url, headers=headers, data = payload)
    res.text.encode('utf8')

    data = res.json()
    temp = data['main']['temp']
    description = data['weather'][0]['description']
    name = data['name']
    humidity = data['main']['humidity']
    read_text('Today in ' + name.replace("Thanh pho", "") + "city" + ', Temperature is: {} degree celcius'.format(
        temp) + ', Humidity : {}'.format(humidity) + ', Mostly: {}'.format(description))

