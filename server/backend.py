import requests
import threading
import re
from googletrans import Translator
from flask import request
from datetime import datetime
from requests import get
from freeGPT import gpt3
from server.auto_proxy import get_random_proxy, remove_proxy, update_working_proxies
from server.config import special_instructions


class Backend_Api:
    def __init__(self, app, config: dict) -> None:
        self.app = app
        self.use_auto_proxy = config['use_auto_proxy']
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }

        if self.use_auto_proxy:
            update_proxies = threading.Thread(
                target=update_working_proxies, daemon=True)
            update_proxies.start()

    def _conversation(self):
        try:
            jailbreak = request.json['jailbreak']
            model = request.json['model']
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

            if special_instructions[jailbreak]:
                set_response_language(
                    prompt['content'], special_instructions[jailbreak])

            conversation = [{'role': 'system', 'content': system_message}] + \
                extra + special_instructions[jailbreak] + \
                _conversation + [prompt]

            def stream():
                if isGPT3Model(model):
                    response = get_response_gpt3(
                        conversation, self.use_auto_proxy)
                if isGPT4Model(model):
                    response = get_response_gpt4(conversation)

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


def filter_jailbroken_response(response):
    response = re.sub(r'GPT:.*?ACT:', '', response, flags=re.DOTALL)
    response = re.sub(r'ACT:', '', response)
    return response


def set_response_language(prompt, special_instructions_list):
    translator = Translator()
    detected_language = translator.detect(prompt).lang
    language_instructions = f"You will respond in the language: {detected_language}. "
    if special_instructions_list:
        special_instructions_list[0]['content'] = language_instructions + \
            special_instructions_list[0]['content']


def get_response_gpt3(conversation, use_proxy):
    while use_proxy:
        try:
            random_proxy = get_random_proxy()
            res = gpt3.Completion.create(
                prompt=conversation, proxy=random_proxy)
            response = res['text']
            break
        except Exception as e:
            print(f"Error with proxy {random_proxy}: {e}")
            remove_proxy(random_proxy)

    while not use_proxy:
        try:
            res = gpt3.Completion.create(prompt=conversation)
            response = res['text']
            break
        except Exception as e:
            print(f"Error: {e}")

    if response is not None:
        response = filter_jailbroken_response(response)
        return response


def get_response_gpt4(conversation):  
    api_url = f"http://127.0.0.1:3000/ask?prompt={conversation}&model=forefront"  
  
    while True:  
        try:  
            res = requests.get(api_url)  
            res.raise_for_status()  
            response = res.text  
            break  
        except Exception as e:  
            print(f"Error: {e}")  
  
    if response is not None:  
        response = filter_jailbroken_response(response)  
        return response  


def isGPT3Model(model):
    return model == "text-gpt-0035"


def isGPT4Model(model):
    return model == "text-gpt-0040"
