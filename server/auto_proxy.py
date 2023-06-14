import random  
import requests  
import time  
import threading  
  
  
def fetch_proxies():  
    """Fetch a list of proxy servers from proxyscrape.com.  
  
    Returns:  
        list: A list of proxy servers in the format "IP:Port".  
    """  
    url = "https://api.proxyscrape.com/v2/?request=displayproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=all"  
    response = requests.get(url)  
    if response.status_code == 200:  
        proxy_list = response.text.split("\r\n")[:-1]  
        return proxy_list  
    else:  
        print(f"Error fetching proxies: {response.status_code}")  
        return []  
  
  
def test_proxy(proxy, prompt, timeout):  
    """Test the given proxy server with a specified prompt and timeout.  
  
    Args:  
        proxy (str): The proxy server in the format "IP:Port".  
        prompt (str): The test prompt to be used for testing.  
        timeout (int): The maximum time in seconds allowed for the test.  
    """  
    try:  
        start_time = time.time()  
        # res = gpt3.Completion.create(prompt=prompt, proxy=proxy)  
        end_time = time.time()  
        response_time = end_time - start_time  
  
        if response_time < timeout:  
            response_time = int(response_time*1000)  
            print(f'proxy: {proxy} [{response_time}ms] ✅')  
            add_working_proxy((proxy))  
    except Exception as e:  
        pass  
  
  
def add_working_proxy(proxy):  
    """Add a working proxy server to the global working_proxies list.  
  
    Args:  
        proxy (str): The proxy server in the format "IP:Port". 
    """  
    global working_proxies  
    working_proxies.append(proxy)  
  
  
def remove_proxy(proxy):  
    """Remove a proxy server from the global working_proxies list.  
  
    Args:  
        proxy (str): The proxy server in the format "IP:Port".  
    """  
    global working_proxies  
    if proxy in working_proxies:  
        working_proxies.remove(proxy)  
  
  
def get_working_proxies(prompt, timeout=5):  
    """Fetch and test proxy servers, adding working proxies to the global working_proxies list.  
  
    Args:  
        prompt (str): The test prompt to be used for testing.  
        timeout (int, optional): The maximum time in seconds allowed for testing. Defaults to 5.  
    """  
    proxy_list = fetch_proxies()  
    threads = []  
  
    for proxy in proxy_list:  
        thread = threading.Thread(target=test_proxy, args=(  
            proxy, prompt, timeout))  
        threads.append(thread)  
        thread.start()  
  
    for t in threads:  
        t.join(timeout)  
  
  
def update_working_proxies():  
    """Continuously update the global working_proxies list with working proxy servers."""  
    global working_proxies  
    test_prompt = "What is the capital of France?"  
  
    while True:  
        working_proxies = []  # Clear the list before updating  
        get_working_proxies(test_prompt)  
        print('proxies updated')  
        time.sleep(1800)  # Update proxies list every 30 minutes  
  
  
def get_random_proxy():  
    """Get a random working proxy server from the global working_proxies list.  
  
    Returns:  
        str: A random working proxy server in the format "IP:Port".  
    """  
    global working_proxies  
    return random.choice(working_proxies)  
