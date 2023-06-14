import os
import json
import time
import subprocess

from ...typing import sha256, Dict, get_type_hints

url = 'https://you.com'
model = 'gpt-3.5-turbo'
supports_stream = True


def _create_completion(model: str, messages: list, stream: bool, **kwargs):

    path = os.path.dirname(os.path.realpath(__file__))
    config = json.dumps({
        'messages': messages[:-1] if len(messages) > 1 else [],
    })

    try:
        subprocess.run(["python3", "--version"],
                       capture_output=True, check=True)
        cmd = ["python3", f"{path}/helpers/you.py", config]
    except subprocess.CalledProcessError:
        cmd = ["python", f"{path}/helpers/you.py", config]

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    for line in iter(p.stdout.readline, b''):
        yield line.decode('utf-8', errors='ignore')  # [:-1]
