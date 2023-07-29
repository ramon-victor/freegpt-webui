import os  
import json
import requests  
from typing import Dict, get_type_hints  
  
url = 'https://ai.fakeopen.com/v1/'  
model = [  
    'gpt-3.5-turbo', 
    'gpt-3.5-turbo-0613',
    'gpt-3.5-turbo-16k', 
    'gpt-3.5-turbo-16k-0613', 
]  

supports_stream = True  
needs_auth = False  
  
  
def _create_completion(model: str, messages: list, stream: bool, **kwargs):  
  
    headers = {  
        'Content-Type': 'application/json',  
        'accept': 'text/event-stream',  
        'Cache-Control': 'no-cache',  
        'Proxy-Connection': 'keep-alive',  
        'Authorization': f"Bearer {os.environ.get('FAKE_OPEN_KEY', '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')}",  
    }  
  
    json_data = {  
        'messages': messages,  
        'temperature': 1.0,  
        'model': model,  
        'stream': stream,  
    }  
  
    response = requests.post(  
        'https://ai.fakeopen.com/v1/chat/completions', headers=headers, json=json_data, stream=True  
    )  
  
    for token in response.iter_lines():  
        decoded = token.decode('utf-8')  
        if decoded == '[DONE]':  
            break  
        if decoded.startswith('data: '):  
            data_str = decoded.replace('data: ', '')  
            if data_str != '[DONE]':  
                data = json.loads(data_str)  
                if 'choices' in data and 'delta' in data['choices'][0] and 'content' in data['choices'][0]['delta']:  
                    yield data['choices'][0]['delta']['content']  


  
  
params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' +  '(%s)' % ', '.join(  
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])  
