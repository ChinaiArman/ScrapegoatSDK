"""
"""

from .gardener import Gardener
from .goat import Goat
from .interpreter import ThistleInterpreter
from .milkmaid import Milkmaid
from .milkman import Milkman


class Shepherd:
    """
    """
    def __init__(self):
        """
        """
        self.gardener = Gardener()
        self.interpreter = ThistleInterpreter()
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
        thistles = self.interpreter.interpret(query)
        results = self.goat.feast(root, thistles)
        return set(results)
