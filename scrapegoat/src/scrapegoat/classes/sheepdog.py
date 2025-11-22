"""
"""
from typing import Union
import requests

from .command import FetchCommand

class Sheepdog:
    """
    """
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Scrapegoat)",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Accept": "*/*",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
    }
    def __init__(self):
        """
        """
        pass

    def fetch(self, fetch_command: Union[str, FetchCommand]) -> str:
        """
        """
        if not isinstance(fetch_command, FetchCommand):
            fetch_command = FetchCommand(fetch_command)
        fetch_command.set_getter(self.getter)
        return fetch_command.execute()
    
    def getter(self, url: str, **kwargs) -> str:
        """
        """
        headers = kwargs.pop('headers', self.DEFAULT_HEADERS)
        response = requests.get(url, headers=headers, **kwargs)
        response.raise_for_status()
        return response.text

def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
