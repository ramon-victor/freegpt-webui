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
        'authority': 'edgeservices.bing.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Microsoft Edge";v="110"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-bitness': '"64"',
        'sec-ch-ua-full-version': '"110.0.1587.69"',
        'sec-ch-ua-full-version-list': '"Chromium";v="110.0.5481.192", "Not A(Brand";v="24.0.0.0", "Microsoft Edge";v="110.0.1587.69"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"15.0.0"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.69',
        'x-edge-shopping-flag': '1',
        'Referer': 'https://chat.ylokh.xyz/',
        'Origin': 'https://chat.ylokh.xyz',
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
            print(data)
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
