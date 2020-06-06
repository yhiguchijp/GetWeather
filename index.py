import urllib.request
from bs4 import BeautifulSoup
import requests
import os

def get_json():
    url = 'http://weather.livedoor.com/forecast/webservice/json/v1?'
    query_params = {'city': '270000'} # 大阪
    data = requests.get(url, params=query_params).json()

    weather_item = []
    weather_item.append(data['title'])

    for weather in data['forecasts']:
        weather_item.append(weather['dateLabel'] + ' ' + weather['date'] + 'の天気：' + weather['telop'] + ' ')
        try:
            weather_item.append(' 最低気温：' + weather['temperature']['min']['celsius'] + '℃')
            weather_item.append(' 最高気温：' + weather['temperature']['max']['celsius'] + '℃')
        except:
            pass
        weather_item.append('\n')

    message = ''.join(weather_item)

    return message

def send_line_notification(message):
    line_notify_token = os.environ['LineTokenMyNotification']
    line_notify_api = 'https://notify-api.line.me/api/notify'
    payload = {'message': message}
    headers = {'Authorization': 'Bearer ' + line_notify_token}  # 発行したトークン
    line_notify = requests.post(line_notify_api, data=payload, headers=headers)

if __name__ == "__main__":
    message = get_json()
    send_line_notification(message=message)
