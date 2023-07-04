import os
import json
import requests
from typing import Dict, get_type_hints

url = 'https://openai-proxy-api.vercel.app/v1/'
model = {
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-0613'
    'gpt-3.5-turbo-16k',
    'gpt-3.5-turbo-16k-0613',
    'gpt-4',
}

supports_stream = True
needs_auth = False


def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58',
        'Referer': 'https://chat.ylokh.xyz/',
        'Origin': 'https://chat.ylokh.xyz',
        'Connection': 'keep-alive',  
    }

    json_data = {
        'messages': messages,
        'temperature': 1.0,
        'model': model,
        'stream': stream,
    }

    response = requests.post(
        'https://openai-proxy-api.vercel.app/v1/chat/completions', headers=headers, json=json_data, stream=True
    )

    for token in response.iter_lines():
        decoded = token.decode('utf-8')
        if decoded.startswith('data: '):
            data_str = decoded.replace('data: ', '')
            data = json.loads(data_str)
            if 'choices' in data and 'delta' in data['choices'][0]:
                delta = data['choices'][0]['delta']
                content = delta.get('content', '')
                finish_reason = delta.get('finish_reason', '')

                if finish_reason == 'stop':
                    break
                if content:
                    yield content


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + '(%s)' % ', '.join(
    [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
