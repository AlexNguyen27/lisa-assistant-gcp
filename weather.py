import requests
from text_to_speech import read_text
from translation import translate_language

# Searching for weather
def weather():
    url = 'https://api.openweathermap.org/data/2.5/weather?id=1566083&appid=a395d3d89b3fc57be94693534c103fe4'
    payload = {}
    headers = {}
    res = requests.request("GET", url, headers=headers, data = payload)
    res.text.encode('utf8')

    data = res.json()
    temp = round(data['main']['temp'] / 10)
    print(data['main'])
    description = data['weather'][0]['description']
    # name = data['name']3
    humidity = data['main']['humidity']
    # todo: need a translate
    read_text('Hôm nay, tại thành phố Hồ Chí Minh, Nhiệt độ là: {} độ C'.format(
        temp) + ', Độ ẩm : {}'.format(humidity) + ' phần trăm, Thời tiết chủ yếu: {}'.format(translate_language(description)))

# weather();
