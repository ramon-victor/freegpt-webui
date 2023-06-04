[![PyPI version](https://badge.fury.io/py/freeGPT.svg)](https://badge.fury.io/py/freeGPT)
[![Downloads](https://static.pepy.tech/personalized-badge/freeGPT?period=month&units=international_system&left_color=grey&right_color=brightgreen&left_text=Downloads)](https://pepy.tech/project/freeGPT)
[![License](https://img.shields.io/badge/License-GPLv3-bright&green.svg)](LICENSE)
# freeGPT
A Python package that gives access to GPT3 &amp; GPT4 models for free.
<br>
Get started by installing the package:
```
py -m pip install --upgrade freeGPT
```

## Source:
*Models with .web have internet access on.*
<br>
| Models            | Websites                                 |
| ----------------- | -----------------------------------------|
| gpt3              | [you.com](https://you.com)               |
| gpt4              | [forefront.ai](https://chat.forefront.ai)|

### TODO-List:
- [x] Add GPT-4.
- [x] Make the library well-documented.
- [x] Make the over-all library easier to use.
- [x] Make the over-all library easier to understand.
- [x] Replace you.com with theb.ai for less failed responses.
- [x] Make GPT-3 & GPT-4 models with web access.
- [x] Add a non-GPT model.
- [ ] Add a text to image generation model.
- [ ] Make a discord bot.

## Support me:
- Join my [Discord Server](https://discord.gg/NcQ26PrNDp) :D
- Star this repository :D

## Examples:

#### Alpaca-7b:
```python
from freeGPT import alpaca

while True:
    prompt = input("👦 > ")
    resp = alpaca.Completion.create(prompt=prompt)
    print(f"🤖 > {resp}")
```
#### GPT-3:
```python
from freeGPT import gpt3

while True:
    prompt = input("👦 > ")
    resp = gpt3.Completion.create(prompt=prompt)
    print(f"🤖 > {resp['text']}")
```
#### GPT-4:
```python
# Uhh, sorry but gpt4 is kinda broken currently, will maybe get fixed in the next update.
from freeGPT import gpt4

while True:
    token = Account.create(logging=True)
    prompt = input("👦 > ")
    resp = gpt4.Completion.create(prompt=prompt, token=token)
    print(f"🤖 > {resp.text}")
```

## Star History:
[![Star History Chart](https://api.star-history.com/svg?repos=Ruu3f/freeGPT&type=Date)](https://github.com/Ruu3f/freeGPT/stargazers)

