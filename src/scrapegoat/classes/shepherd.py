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
    
    def herd(self, query: str, root=None) -> list:
        """
        """
        goatspeak = self.interpreter.interpret_from_string(query)
        query_obj = goatspeak.query_list[0]
        
        if root is None:
            html = self.sheepdog.fetch(goatspeak.fetch_command)
            root = self.gardener.grow_tree(html)
        
        results = self.goat.feast(root, query_obj.graze_commands)

        if query_obj.churn_command:
            self.milkmaid.churn(results, query_obj.churn_command)

        if query_obj.deliver_command:
            self.milkman.deliver(results, query_obj.deliver_command)

        return list(dict.fromkeys(results))

    def herd_from_file(self, file_path: str) -> None:
        """
        """
        pass
    
    def herd_from_html(self, raw_html: str, query: str) -> list:
        """
        """
        root = self.gardener.grow_tree(raw_html)
        return self.herd(query, root=root)
    
    def herd_from_node(self, root, query: str) -> list:
        """
        """
        return self.herd(query, root=root)

def main():
    """
    """
    pass


if __name__ == "__main__":
    main()
