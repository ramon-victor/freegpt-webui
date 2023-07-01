import os, requests, uuid
from ...typing import sha256, Dict, get_type_hints

url = 'https://mishalsgpt.vercel.app'
model = ['gpt-3.5-turbo-16k-0613', 'gpt-3.5-turbo']
supports_stream = True
needs_auth = False

def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        'model': model,
        'temperature': 0.7,
        'messages': messages
    }
    response = requests.post(url + '/api/openai/v1/chat/completions', 
                             headers=headers, json=data, stream=True)
    yield response.json()['choices'][0]['message']['content']

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
