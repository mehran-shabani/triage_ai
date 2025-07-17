import json
import time
import requests
from django.conf import settings

TALKBOT_URL = 'https://api.talkbot.ir/v1/chat/completions'


def talkbot_complete(messages, retries: int = 3):
    """Call the TalkBot API with basic retry logic."""
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings.TALKBOT_API_KEY}'
    }
    payload = json.dumps({
        'model': 'gpt-4o-mini',
        'messages': messages,
        'max_tokens': 4000,
        'temperature': 0.3,
        'stream': False,
        'top_p': 1.0,
        'frequency_penalty': 0.0,
        'presence_penalty': 0.0
    })
    for _ in range(retries):
        try:
            response = requests.post(
                TALKBOT_URL, headers=headers, data=payload, timeout=10
            )
            if response.status_code == 200:
                return response.json()
        except requests.RequestException:
            time.sleep(1)
    return {"error": "TalkBot request failed"}

__all__ = ["talkbot_complete"]
