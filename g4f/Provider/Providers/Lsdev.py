import os, uuid, requests
from ...typing import sha256, Dict, get_type_hints

url = 'https://gpt.free.lsdev.me'
model = ['gpt-4-0613', 'gpt-4-poe']
supports_stream = True
needs_auth = True

models = {
    'gpt-4-0613': {
        "id":"gpt-4-0613",
        "name":"GPT-4-0613",
        "maxLength":24000,
        "tokenLimit":8192
    },
    'claude-instant-100k': {
        "id":"claude-instant-100k",
        "name":"CLAUDE-INSTANT-100K"
    },
    'gpt-4-poe': {
        "id":"gpt-4-poe",
        "name":"GPT-4-POE"
    },
}

def _create_completion(model: str, messages: list, stream: bool, chatId: str, **kwargs):

    print(kwargs)

    headers = {
        'authority': 'gpt.free.lsdev.me',
        'content-type': 'application/json',
        'origin': 'https://gpt.free.lsdev.me',
        'referer': 'https://gpt.free.lsdev.me/zh',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    json_data = {
        'conversationId': chatId,
          'model': models[model],
          'messages': messages,
          'auth': 'oVy1CLB25mA43',
          'key': '',
          'prompt': "You are ChatGPT, a large language model trained by OpenAI. Follow the user's instructions carefully. Respond using markdown.",
      }

    response = requests.post('https://gpt.free.lsdev.me/api/chat', 
                             headers=headers, json=json_data, stream=stream)

    for token in response.iter_content(chunk_size=2046):
        yield (token.decode('utf-8'))

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])