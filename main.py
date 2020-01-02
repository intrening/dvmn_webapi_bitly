import requests
import os
import argparse
from dotenv import load_dotenv


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


def main():
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')
    
    parser = argparse.ArgumentParser(description='Сокращение ссылок через Bitly')
    parser.add_argument('url', help='Ваша ссылка')
    args = parser.parse_args()
    url = args.url

    if url.startswith('bit.ly'):
        try:
            print('Кол-во кликов в битлинке ', url, ' - ', count_clicks(bitly_token, url))
        except requests.exceptions.HTTPError:
            print ('Ошибка в битлинке')
    else:
        try:
            print('Битлинк ', shorten_link(bitly_token, url))
        except requests.exceptions.HTTPError:
            print ('Ошибка в ссылке')


if __name__ == '__main__':
    main()
