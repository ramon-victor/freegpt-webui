import os
import requests
from ...typing import sha256, Dict, get_type_hints

url = 'https://chat.pierangelo.info'
model = ['gpt-4', 'gpt-3.5-turbo']
supports_stream = True

models = {
    'gpt-4': {
        'id':'gpt-4',
        'name':'GPT-4'
    },
    'gpt-3.5-turbo': {
        'id':'gpt-3.5-turbo',
        'name':'GPT-3.5'
    }
}

def _create_completion(model: str, messages: list, stream: bool, **kwargs):

    headers = {
        'authority': 'chat.pierangelo.info',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://chat.pierangelo.info',
        'pragma': 'no-cache',
        'referer': 'https://chat.pierangelo.info/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    json_data = {
        'model': models[model],
        'messages': messages,
        'key': '',
        'prompt': "You are ChatGPT, a large language model trained by OpenAI. Answer consisely",
        'temperature': 0.7
    }

    response = requests.post('https://chat.pierangelo.info/api/chat', 
                             headers=headers, json=json_data, stream=True)
    
    for token in response:
        yield (token)

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f'{name}: {get_type_hints(_create_completion)[name].__name__}' for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])