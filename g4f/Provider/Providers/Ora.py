import os, requests, uuid
from ...typing import sha256, Dict, get_type_hints

url = 'https://ora.ai'
model = ['gpt-3.5-turbo', 'gpt-4']
supports_stream = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    headers = {
        'authority': 'ora.ai',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'content-type': 'application/json',
        'origin': 'https://ora.ai',
        'pragma': 'no-cache',
        'referer': 'https://ora.ai/chat/',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
    }

    json_data = {
        'chatbotId': 'adb2b793-e667-46b9-8d80-114eaa9a4c40',
        'input': messages[-1]['content'],
        'userId': f'auto:{uuid.uuid4()}',
        'provider': 'OPEN_AI',
        'config': False,
        'includeHistory': False
    }

    response = requests.post('https://ora.ai/api/conversation', 
                            headers=headers, json=json_data)
    
    yield response.json()['response']

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])