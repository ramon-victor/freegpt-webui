import re
import os
import openai
import openai.error
from dotenv import load_dotenv
from ...typing import sha256, Dict, get_type_hints

load_dotenv()
api_key_env = os.environ.get("CHIMERA_API_KEY") or os.environ.get("NAGA_API_KEY")
openai.api_base = "https://api.naga.ac/v1"

url = 'https://api.naga.ac'
model = [
    'gpt-3.5-turbo',
    'gpt-3.5-turbo-0301',
    'gpt-3.5-turbo-16k',
    'gpt-4',
    'gpt-4-0314',
    'gpt-4-32k',
    'llama-2-70b-chat',
    'oasst-sft-6-llama-30b',
    'claude-instant',
    'claude-2',
    'claude-2-100k'
]
supports_stream = True
needs_auth = False


def _create_completion(model: str, messages: list, stream: bool, api_key: str = None, **kwargs):

    openai.api_key = api_key if api_key else api_key_env

    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=messages,
            stream=stream
        )

        if (stream):
            for chunk in response:
                yield chunk.choices[0].delta.get("content", "")
        else:
            yield response.choices[0].message.get("content", "")

    except openai.error.APIError as e:
        detail_pattern = re.compile(r'{"detail":"(.*?)"}')
        match = detail_pattern.search(e.user_message)
        if match:
            error_message = match.group(1)
            print(error_message)
            yield error_message
        else:
            print(e.user_message)
            yield e.user_message


params = f'g4f.Providers.{os.path.basename(__file__)[:-3]} supports: ' + \
    '(%s)' % ', '.join(
        [f"{name}: {get_type_hints(_create_completion)[name].__name__}" for name in _create_completion.__code__.co_varnames[:_create_completion.__code__.co_argcount]])
