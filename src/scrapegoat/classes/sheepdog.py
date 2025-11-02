"""
"""
from typing import Union

from .command import FetchCommand

class Sheepdog:
    """
    """
    def __init__(self):
        """
        """
        pass

    def fetch(self, fetch_command: Union[str, FetchCommand]) -> str:
        """
        """
        if not isinstance(fetch_command, FetchCommand):
            fetch_command = FetchCommand(fetch_command)
        return fetch_command.execute()
    

def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
