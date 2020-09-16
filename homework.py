import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

TWILIO_SID = os.getenv('tTWILIO_SID')
TWILIO_TOKEN = os.getenv('TWILIO_TOKEN')
NUMBER_FROM = os.getenv('NUMBER_FROM')
NUMBER_TO = os.getenv('NUMBER_TO')
VK_TOKEN = os.getenv('VK_TOKEN')

client = Client(TWILIO_SID, TWILIO_TOKEN)


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'v': 5.92,
        'access_token': VK_TOKEN,
        'fields': 'online'
    }
    response = requests.post(
        'https://api.vk.com/method/users.get',
        params=params
    ).json().get('response')
    status = response[0]['online']
    return status


def sms_sender(sms_text):
    message = client.messages.create(
        body=sms_text,
        from_=NUMBER_FROM,
        to=NUMBER_TO
    )
    return message.sid


if __name__ == "__main__":
    vk_id = input('Введите id')
    while True:
        if get_status(vk_id) == 1:
            sms_sender(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
