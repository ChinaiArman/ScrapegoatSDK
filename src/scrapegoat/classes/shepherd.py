"""
"""

import os

from .gardener import Gardener
from .goat import Goat
from .interpreter import Interpeter
from .milkmaid import Milkmaid
from .milkman import Milkman
from .sheepdog import Sheepdog


class Shepherd:
    """
    """
    def __init__(self):
        """
        """
        self.gardener = Gardener()
        self.interpreter = Interpeter()
        self.sheepdog = Sheepdog()
        self.goat = Goat()
        self.milkmaid = Milkmaid()
        self.milkman = Milkman()
    
    def herd(self, query: str) -> list:
        """
        """
        goatspeak = self._convert_query_to_goatspeak(query)

        results = []

        for block in goatspeak:
            html = self.sheepdog.fetch(block.fetch_command)
            root = self.gardener.grow_tree(html)
            self._query_list_handler(block.query_list, root, results)

        return list(dict.fromkeys(results))
    
    def _convert_query_to_goatspeak(self, query: str) -> None:
        """
        """
        if os.path.isfile(query):
            try:
                return self.interpreter.interpret(self.milkman.receive(query))
            except Exception as e:
                raise e
        try:
            return self.interpreter.interpret(query)
        except Exception as e:
            raise e
            
            

    def _query_list_handler(self, query_list: str, root, results) -> list:
        """
        """
        for query in query_list:
            query_results = (self.goat.feast(root, query.graze_commands))
            if query.churn_command:
                self.milkmaid.churn(query_results, query.churn_command)

            results.extend(query_results)

            if query.deliver_command:
                self.milkman.deliver(results, query.deliver_command)
                results.clear()
        return
        
    def _local_herd(self, query: str, root) -> list:
        """
        """
        goatspeak = self._convert_query_to_goatspeak(query)

        results = []

        for block in goatspeak:
            self._query_list_handler(block.query_list, root, results)
                
        return list(dict.fromkeys(results))
    
    def herd_from_node(self, query: str, root) -> list:
        """
        """
        return self._local_herd(query, root=root)
    
    def herd_from_html(self, query: str, html: str) -> list:
        """
        """
        root = self.gardener.grow_tree(html)
        return self._local_herd(query, root=root)
    
    def herd_from_url(self, query: str, url: str) -> list:
        """
        """
        html = self.sheepdog.fetch(url)
        root = self.gardener.grow_tree(html)
        return self._local_herd(query, root=root)

def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
