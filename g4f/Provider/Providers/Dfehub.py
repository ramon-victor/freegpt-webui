import os
import requests
from ...typing import sha256, Dict, get_type_hints

url = "https://chat.dfehub.com"
model = ['gpt-3.5-turbo', 'gpt-3.5-turbo-16k', 'gpt-4']
supports_stream = True
needs_auth = False


def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    headers = {
        'Authority': 'chat.dfehub.com',
        'Content-Type': 'application/json',
        'Method': 'POST',
        'Path': '/api/openai/v1/chat/completions',
        'Scheme': 'https',
        'Accept': 'text/event-stream',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,zh-CN;q=0.6,zh;q=0.5',
        'Content-Type': 'application/json',
        'Origin': 'https://chat.dfehub.com',
        'Referer': 'https://chat.dfehub.com/',
        'Sec-Ch-Ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'Sec-Ch-Ua-Mobile': '?0',
        'Sec-Ch-Ua-Platform': '"Windows"',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest',
    }

    data = {
        'model': model,
        'temperature': 0.7,
        'max_tokens': '8000',
        'presence_penalty': 0,
        'messages': messages,
    }
    
    response = requests.post(url + '/api/openai/v1/chat/completions',
                             headers=headers, json=data, stream=stream)

    yield response.json()['choices'][0]['message']['content']


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
