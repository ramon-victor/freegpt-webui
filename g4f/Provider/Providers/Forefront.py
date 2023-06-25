import os
import json
import requests
from ...typing import sha256, Dict, get_type_hints

url = 'forefront.com'
model = ['gpt-3.5-turbo', 'gpt-4']
supports_stream = True


def _create_completion(model: str, messages: list, stream: bool, **kwargs):
    """ Create a completion request for Forefront API """
    json_data = {
        'text': messages[-1]['content'],
        'action': 'noauth',
        'id': '',
        'parentId': '',
        'workspaceId': '',
        'messagePersona': '607e41fe-95be-497e-8e97-010a59b2e2c0',
        'model': model,
        'messages': messages[:-1] if len(messages) > 1 else [],
        'internetMode': 'auto'
    }
    
    response = requests.post('https://streaming.tenant-forefront-default.knative.chi.coreweave.com/free-chat',
                             json=json_data, stream=True)

    for token in response.iter_lines():
        if b'delta' in token:
            yield json.loads(token.decode().split('data: ')[1])['delta']


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in 
         _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
