"""
"""

from scrapegoat import Shepherd, Gardener, Sheepdog
from scrapegoat_loom import Loom



class NewSheepDog(Sheepdog):
    """
    """
    def getter(self, url: str, **kwargs) -> str:
        """
        """
        print(f"Fetching URL: {url}")
        return super().getter(url, **kwargs)

def main():
    """
    """
    # SHEPHERD EXAMPLE
    shepherd = Shepherd(sheepdog=NewSheepDog())
    shepherd.herd("example.goat")

    # LOOM EXAMPLE
    # html = Sheepdog().fetch("https://en.wikipedia.org/wiki/Web_scraping")
    # root = Gardener().grow_tree(html)
    # Loom(root).weave()


if __name__ == "__main__":
    main()
