import sys
import uuid
import json
import browser_cookie3

from curl_cffi import requests

config = json.loads(sys.argv[1])

def session_auth(cookies):
    headers = {
        'authority': 'chat.openai.com',
        'accept': '*/*',
        'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'referer': 'https://chat.openai.com/chat',
        'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
    }

    return requests.get('https://chat.openai.com/api/auth/session', 
                        cookies=cookies, headers=headers, impersonate='chrome110').json()

all_cookies = {cookie.name: cookie.value for cookie in browser_cookie3.chrome(
    domain_name='chat.openai.com')}

try:
    cookies = {
        '__Secure-next-auth.session-token': all_cookies['__Secure-next-auth.session-token'],
    }
except Exception:
    print('Failed to get "__Secure-next-auth.session-token" in chrome, please make sure you are authenticated on openai.com')
    exit(0)

headers = {
    'authority': 'chat.openai.com',
    'accept': 'text/event-stream',
    'accept-language': 'en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3',
    'authorization': 'Bearer ' + session_auth(cookies)['accessToken'],
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'origin': 'https://chat.openai.com',
    'pragma': 'no-cache',
    'referer': 'https://chat.openai.com/chat',
    'sec-ch-ua': '"Chromium";v="112", "Google Chrome";v="112", "Not:A-Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
}

payload = {
    'action': 'next',
    'history_and_training_disabled': False,
    'messages': [
        {
            'id': str(uuid.uuid4()),
            'author': {
                'role': 'user',
            },
            'content': {
                'content_type': 'text',
                'parts': [
                    config['messages'][-1]['content']
                ]
            }
        }
    ],
    'model': 'text-davinci-002-render-sha',
    'parent_message_id': str(uuid.uuid4()),
    'supports_modapi': True,
    'timezone_offset_min': -60
}

completion = ''

def format(chunk):
    try:
        global completion
        
        if b'parts' in chunk:
            json_data = json.loads(chunk.decode('utf-8').split('data: ')[1])
            token = json_data['message']['content']['parts'][0]
            token = token.replace(completion, '')
            completion += token
        
            print(token, flush=True, end = '')
            
    except Exception as e:
        pass

for _ in range(3):
    try:
        response = requests.post('https://chat.openai.com/backend-api/conversation', 
                                json=payload, headers=headers, content_callback=format, impersonate='chrome110')
        break
    except:
        continue