import os, re, json

try:
    from tls_client import Session
except ImportError:
    os.system("pip install tls_client --no-cache-dir")
from uuid import uuid4
from pydantic import BaseModel
from fake_useragent import UserAgent
from typing import Optional, List, Dict, Any


class Completion:
    """A class that provides methods for creating completion requests."""

    @staticmethod
    def create(
        prompt: str,
        page: int = 1,
        count: int = 10,
        safe_search: str = "Moderate",
        on_shopping_page: bool = False,
        mkt: str = "",
        response_filter: str = "WebPages,Translations,TimeZone,Computation,RelatedSearches",
        domain: str = "youchat",
        query_trace_id: str = None,
        chat: List[str] = None,
        include_links: bool = False,
        detailed: bool = False,
        proxy: Optional[str] = None,
    ) -> dict:
        """
        Creates a completion request.

        Args:
            prompt (str): The prompt text for the completion.
            page (int, optional): The page number for pagination. Defaults to 1.
            count (int, optional): The number of results per page. Defaults to 10.
            safe_search (str, optional): The safe search level. Defaults to 'Moderate'.
            on_shopping_page (bool, optional): Indicates if the completion is on a shopping page. Defaults to False.
            mkt (str, optional): The market for the completion. Defaults to ''.
            response_filter (str, optional): The filter for the response. Defaults to 'WebPages,Translations,TimeZone,Computation,RelatedSearches'.
            domain (str, optional): The domain for the completion. Defaults to 'youchat'.
            query_trace_id (str, optional): The trace ID for the query. Defaults to None.
            chat (list, optional): A list of chat messages. Defaults to None.
            include_links (bool, optional): Indicates if links should be included in the response. Defaults to False.
            detailed (bool, optional): Indicates if detailed results should be included in the response. Defaults to False.
            proxy (str, optional): The proxy server to use. Defaults to None.

        Returns:
            dict: The completion response as a dictionary.

        Raises:
            Exception: If unable to get the response.
        """
        if chat is None:
            chat = []

        proxies = (
            {"http": "http://" + proxy, "https": "http://" + proxy} if proxy else {}
        )

        client = Session(client_identifier="chrome_108")
        client.headers = Completion.__get_headers()
        client.proxies = proxies

        response = client.get(
            f"https://you.com/api/streamingSearch",
            params={
                "q": prompt,
                "page": page,
                "count": count,
                "safeSearch": safe_search,
                "onShoppingPage": on_shopping_page,
                "mkt": mkt,
                "responseFilter": response_filter,
                "domain": domain,
                "queryTraceId": str(uuid4())
                if query_trace_id is None
                else query_trace_id,
                "chat": str(chat),
            },
        )

        if "youChatToken" not in response.text:
            raise Exception("Unable to fetch the response.")

        you_chat_serp_results = re.search(
            r"(?<=event: youChatSerpResults\ndata:)(.*\n)*?(?=event: )", response.text
        ).group()
        third_party_search_results = re.search(
            r"(?<=event: thirdPartySearchResults\ndata:)(.*\n)*?(?=event: )",
            response.text,
        ).group()

        text = "".join(re.findall(r'{"youChatToken": "(.*?)"}', response.text))

        extra = {
            "youChatSerpResults": json.loads(you_chat_serp_results),
        }

        result = {
            "text": text.replace("\\n", "\n").replace("\\\\", "\\").replace('\\"', '"')
        }

        if include_links:
            result["links"] = json.loads(third_party_search_results)["search"][
                "third_party_search_results"
            ]

        if detailed:
            result["extra"] = extra

        return result

    @staticmethod
    def __get_headers() -> dict:
        """
        Returns the headers for the completion request.

        Returns:
            dict: The headers as a dictionary.
        """
        return {
            "authority": "you.com",
            "accept": "text/event-stream",
            "accept-language": "en,fr-FR;q=0.9,fr;q=0.8,es-ES;q=0.7,es;q=0.6,en-US;q=0.5,am;q=0.4,de;q=0.3",
            "cache-control": "no-cache",
            "referer": "https://you.com/search?q=who+are+you&tbm=youchat",
            "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "cookie": f"safesearch_guest=Moderate; uuid_guest={str(uuid4())}",
            "user-agent": UserAgent().random,
        }
