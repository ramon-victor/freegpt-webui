import re
import time
import g4f
from g4f import ChatCompletion
from googletrans import Translator
from flask import request, Response, stream_with_context
from datetime import datetime
from requests import get
from server.config import special_instructions


class Backend_Api:
    def __init__(self, bp, config: dict) -> None:
        """
        Initialize the Backend_Api class.
        :param app: Flask application instance
        :param config: Configuration dictionary
        """
        self.bp = bp
        self.routes = {
            '/backend-api/v2/conversation': {
                'function': self._conversation,
                'methods': ['POST']
            }
        }
        
    def _conversation(self):
        """
        Handles the conversation route.

        :return: Response object containing the generated conversation stream
        """
        max_retries = 3
        retries = 0
        conversation_id = request.json['conversation_id']

        while retries < max_retries:
            try:
                jailbreak = request.json['jailbreak']
                model = request.json['model']
                messages = build_messages(jailbreak)

                # Generate response
                response = ChatCompletion.create(
                    model=model,
                    stream=True,
                    chatId=conversation_id,
                    messages=messages
                )

                return Response(stream_with_context(generate_stream(response, jailbreak)), mimetype='text/event-stream')

            except Exception as e:
                print(e)
                print(e.__traceback__.tb_next)

                retries += 1
                if retries >= max_retries:
                    return {
                        '_action': '_ask',
                        'success': False,
                        "error": f"an error occurred {str(e)}"
                    }, 400
                time.sleep(3)  # Wait 3 second before trying again


def build_messages(jailbreak):
    """
    Build the messages for the conversation.

    :param jailbreak: Jailbreak instruction string
    :return: List of messages for the conversation
    """
    _conversation = request.json['meta']['content']['conversation']
    internet_access = request.json['meta']['content']['internet_access']
    prompt = request.json['meta']['content']['parts'][0]

    # Generate system message
    current_date = datetime.now().strftime("%Y-%m-%d")
    system_message = (
        f'You are ChatGPT also known as ChatGPT, a large language model trained by OpenAI. '
        f'Strictly follow the users instructions. '
        f'Knowledge cutoff: 2021-09-01 Current date: {current_date}. '
        f'{set_response_language(prompt)}'
    )

    # Initialize the conversation with the system message
    conversation = [{'role': 'system', 'content': system_message}]

    # Add the existing conversation
    conversation += _conversation

    # Add web results if enabled
    conversation += fetch_search_results(
        prompt["content"]) if internet_access else []

    # Add jailbreak instructions if enabled
    if jailbreak_instructions := getJailbreak(jailbreak):
        conversation += jailbreak_instructions

    # Add the prompt
    conversation += [prompt]

    # Reduce conversation size to avoid API Token quantity error
    conversation = conversation[-4:] if len(conversation) > 3 else conversation

    return conversation


def fetch_search_results(query):
    """
    Fetch search results for a given query.

    :param query: Search query string
    :return: List of search results
    """
    search = get('https://ddg-api.herokuapp.com/search',
                 params={
                     'query': query,
                     'limit': 3,
                 })

    snippets = ""
    for index, result in enumerate(search.json()):
        snippet = f'[{index + 1}] "{result["snippet"]}" URL:{result["link"]}.'
        snippets += snippet
    return [{'role': 'system', 'content': snippets}]


def generate_stream(response, jailbreak):
    """
    Generate the conversation stream.

    :param response: Response object from ChatCompletion.create
    :param jailbreak: Jailbreak instruction string
    :return: Generator object yielding messages in the conversation
    """
    if getJailbreak(jailbreak):
        response_jailbreak = ''
        jailbroken_checked = False
        for message in response:
            response_jailbreak += message
            if jailbroken_checked:
                yield message
            else:
                if response_jailbroken_success(response_jailbreak):
                    jailbroken_checked = True
                if response_jailbroken_failed(response_jailbreak):
                    yield response_jailbreak
                    jailbroken_checked = True
    else:
        yield from response


def response_jailbroken_success(response: str) -> bool:
    """Check if the response has been jailbroken.

    :param response: Response string
    :return: Boolean indicating if the response has been jailbroken
    """
    act_match = re.search(r'ACT:', response, flags=re.DOTALL)
    return bool(act_match)


def response_jailbroken_failed(response):
    """
    Check if the response has not been jailbroken.

    :param response: Response string
    :return: Boolean indicating if the response has not been jailbroken
    """
    return False if len(response) < 4 else not (response.startswith("GPT:") or response.startswith("ACT:"))


def set_response_language(prompt):
    """  
    Set the response language based on the prompt content.  

    :param prompt: Prompt dictionary  
    :return: String indicating the language to be used for the response  
    """
    translator = Translator()
    max_chars = 256
    content_sample = prompt['content'][:max_chars]
    detected_language = translator.detect(content_sample).lang
    return f"You will respond in the language: {detected_language}. "


def getJailbreak(jailbreak):
    """  
    Check if jailbreak instructions are provided.  

    :param jailbreak: Jailbreak instruction string  
    :return: Jailbreak instructions if provided, otherwise None  
    """
    if jailbreak != "default":
        special_instructions[jailbreak][0]['content'] += special_instructions['two_responses_instruction']
        if jailbreak in special_instructions:
            special_instructions[jailbreak]
            return special_instructions[jailbreak]
        else:
            return None
    else:
        return None
