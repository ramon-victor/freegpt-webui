import sys

from .typing import MetaModels, Union
from . import Provider

class Model(metaclass=MetaModels):
    
    class model:
        name: str
        base_provider: str
        best_site: str
    
    class gpt_35_turbo:
        name: str = 'gpt-3.5-turbo'
        base_provider: str = 'openai'
        best_site: Provider.Provider = Provider.Forefront

    class gpt_4:
        name: str = 'gpt-4'
        base_provider: str = 'openai'
        best_site: Provider.Provider = Provider.Bing
        
    class davinvi_003:
        name: str = 'davinvi-003'
        base_provider: str = 'openai'
        best_site: Provider.Provider = Provider.Forefront
        
class Utils:
    convert: dict = {
        'gpt-3.5-turbo': Model.gpt_35_turbo,
        'gpt-4': Model.gpt_4
    }

class ChatCompletion:
    @staticmethod
    def create(model: Model.model or str, messages: list, provider: Provider.Provider = None, stream: bool = False, **kwargs):
        try:
            if isinstance(model, str):
                model = Utils.convert[model]

            engine = model.best_site if not provider else provider
            if not engine.supports_stream and stream:
                print(
                    f"ValueError: {engine.__name__} does not support 'stream' argument", file=sys.stderr)
                sys.exit(1)

            return (engine._create_completion(model.name, messages, stream, **kwargs)
                    if stream else ''.join(engine._create_completion(model.name, messages, stream, **kwargs)))

        except TypeError as e:
            print(e)
            arg: str = str(e).split("'")[1]
            print(
                f"ValueError: {engine.__name__} does not support '{arg}' argument", file=sys.stderr)
            sys.exit(1)
