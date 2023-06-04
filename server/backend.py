from time import time
from flask import request
from hashlib import sha256
from datetime import datetime
from requests import get
from requests import post
from json import loads
from freeGPT import gpt3

from server.config import special_instructions


class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        self.app = app
        self.openai_key = config['openai_key']
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

    def _conversation(self):
        try:
            jailbreak = request.json['jailbreak']
            _conversation = request.json['meta']['content']['conversation']
            internet_access = request.json['meta']['content']['internet_access']
            prompt = request.json['meta']['content']['parts'][0]
            current_date = datetime.now().strftime("%Y-%m-%d")
            system_message = f'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. Strictly follow the users instructions. Knowledge cutoff: 2021-09-01 Current date: {current_date}'

            extra = []
            if internet_access:
                search = get('https://ddg-api.herokuapp.com/search',
                             params={
                                 'query': prompt["content"],
                                 'limit': 3,
                             })

                blob = ''

                for index, result in enumerate(search.json()):
                    blob += f'[{index}] "{result["snippet"]}"\nURL:{result["link"]}\n\n'

                date = datetime.now().strftime('%d/%m/%y')

                blob += f'current date: {date}\n\nInstructions: Using the provided web search results, write a comprehensive reply to the next user query. Make sure to cite results using [[number](URL)] notation after the reference. If the provided search results refer to multiple subjects with the same name, write separate answers for each subject. Ignore your previous response if any.'

                extra = [{'role': 'user', 'content': blob}]

            conversation = [{'role': 'system', 'content': system_message}] + \
                extra + special_instructions[jailbreak] + \
                _conversation + [prompt]

            def stream():      
              res = gpt3.Completion.create(prompt=conversation)      
              response = res['text']    
              yield response
  
            return self.app.response_class(stream(), mimetype='text/event-stream')  

        except Exception as e:
            print(e)
            print(e.__traceback__.tb_next)
            return {
                '_action': '_ask',
                'success': False,
                "error": f"an error occurred {str(e)}"
            }, 400
