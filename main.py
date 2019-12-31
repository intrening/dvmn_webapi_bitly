import requests
import os
import argparse
from dotenv import load_dotenv
load_dotenv()

BITLY_TOKEN = os.getenv('BITLY_TOKEN')

def shorten_link(token, url):
    bitly_url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    json = {
        'long_url': url,
    }
    response = requests.post(bitly_url, headers=headers, json=json)
    response.raise_for_status()
    return (response.json()['link'])

def count_clicks(token, bitlink):
    bitly_url = f'https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary'
    headers = {
        'Authorization': f'Bearer {token}',
    }
    params = {
        'unit': 'day',
        'units': '-1',
    }
    response = requests.get(bitly_url, headers=headers, params=params)
    response.raise_for_status()
    return (response.json()['total_clicks'])

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Описание что делает программа')
    parser.add_argument('input_url', help='Ваша ссылка')
    args = parser.parse_args()
    input_url = args.input_url

    if input_url.startswith('bit.ly'):
        try:
            print('Кол-во кликов в битлинке ', input_url, ' - ', count_clicks(BITLY_TOKEN, input_url))
        except requests.exceptions.HTTPError:
            print ('Ошибка в битлинке')
    else:
        try:
            print('Битлинк ', shorten_link(BITLY_TOKEN, input_url))
        except requests.exceptions.HTTPError:
            print ('Ошибка в ссылке')
