

import requests
from pic_api import random_image
from read_table import get_msg
import env


def start():
    '''Начало скрипта'''

    # получаем сообщение
    msg = get_msg()
    if not msg:
        return
    # получаем картинку
    pic = random_image()

    # параметры для отправки в тг
    url = f'https://api.telegram.org/bot{env.TG_TOKEN}/sendPhoto'
    image_data = requests.get(pic).content

    files = {
        'photo': ('image.jpg', image_data)
    }

    params = {
        'chat_id': env.CHAT_ID,
        'caption': msg
    }

    # отправка в тг
    requests.post(url, params=params, files=files)


if __name__ == '__main__':
    start()
