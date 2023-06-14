from typing import Dict, NewType, Union, Optional, List, get_type_hints

sha256 = NewType('sha_256_hash', str)

class MetaModels(type):
    def __str__(cls):
        output: List = [
            f'class Engines:\n',
            f'  class {cls.gpt_35_turbo.__name__}:',
            '    ...',
            f'  class {cls.gpt_4.__name__}:',
            '    ...'
        ]
        
        return '\n'.join(output)