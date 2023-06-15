import os
import requests

from ...typing import sha256, Dict, get_type_hints

url = 'https://4aiu6ctrknfxkoaigkigzh5lwm0cciuc.lambda-url.ap-east-1.on.aws/chat/completions'
model = ['gpt-3.5-turbo', 'gpt-4']
supports_stream = False

class Auth(requests.auth.AuthBase):
    def __init__(self):
        self.token = 'sk-1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKL'
        
    def __call__(self, r):
        r.headers["authorization"] = f"Bearer {self.token}"
        return r

def _create_completion(model: str, messages: list, stream: bool, **kwargs):

    response = requests.post(url, 
        auth=Auth(), json={"model": model,"messages": messages})

    yield (response.json()['choices'][0]['message']['content'])

params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join([f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])