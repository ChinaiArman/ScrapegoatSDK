"""
"""

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
        goatspeak = self.interpreter.interpret(query)

        results = []

        for block in goatspeak:
            html = self.sheepdog.fetch(block.fetch_command)
            root = self.gardener.grow_tree(html)

            for query in block.query_list:
                query_results = (self.goat.feast(root, query.graze_commands))
                if query.churn_command:
                    self.milkmaid.churn(query_results, query.churn_command)

                if query.deliver_command:
                    self.milkman.deliver(query_results, query.deliver_command)

                results.extend(query_results)

        return list(dict.fromkeys(results))

    def herd_from_file(self, file_path: str) -> None:
        """
        """
        pass
    
    def herd_from_html(self, query: str, html: str) -> list:
        """
        """
        root = self.gardener.grow_tree(html)
        return self.herd(query, root=root)
    
    def herd_from_node(self, query: str, root) -> list:
        """
        """
        return self.herd(query, root=root)

def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
