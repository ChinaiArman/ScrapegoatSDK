"""
"""

from .gardener import Gardener
from .goat import Goat
from .interpreter import Interpeter
from .milkmaid import Milkmaid
from .milkman import Milkman


class Shepherd:
    """
    """
    def __init__(self):
        """
        """
        self.gardener = Gardener()
        self.interpreter = Interpeter()
        self.goat = Goat()
        self.milkmaid = Milkmaid()
        self.milkman = Milkman()

    def pasture(self, raw_html: str):
        """
        """
        self.gardener.grow_tree(raw_html)
        return self.gardener.get_root()
    
    def herd(self, root, query: str) -> set:
        """
        """
        commands = self.interpreter.interpret(query)
        results = self.goat.feast(root, commands)
        return set(results)
