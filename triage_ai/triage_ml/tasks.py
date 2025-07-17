import os
import json
import requests
from django.conf import settings

TALKBOT_URL = 'https://api.talkbot.ir/v1/chat/completions'


def talkbot_complete(messages):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.TALKBOT_API_KEY}'
    }
    payload = json.dumps({
        'model': 'gpt-4o-mini',
        'messages': messages,
        'max-token': 4000,
        'temperature': 0.3,
        'stream': False,
        'top_p': 1.0,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    })
    response = requests.post(TALKBOT_URL, headers=headers, data=payload)
    return response.json()
