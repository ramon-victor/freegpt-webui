import requests
import os
import json
from ...typing import sha256, Dict, get_type_hints

url = 'https://hteyun.com'
model = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo-0613']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, temperature: float = 0.7, **kwargs):
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,ja;q=0.6,zh-TW;q=0.5,zh;q=0.4',
        'Origin': 'https://hteyun.com',
        'Referer': 'https://hteyun.com/chat/',
    }
    data = {
        'messages': messages,
        'model': model,
        'systemMessage': 'You are ChatGPT, a large language model trained by OpenAI. Follow the user\'s instructions carefully. Respond using russian language.',
        'temperature': 0.7,
        'presence_penalty': 0,
    }
    response = requests.post(url + '/api/chat-stream', json=data, headers=headers, stream=True)
    print(response.json())

    # Извлечение текста из response
    return response.json()['text']


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
