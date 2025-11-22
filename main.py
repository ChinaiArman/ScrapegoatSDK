"""
"""

from scrapegoat import Shepherd, Gardener, Sheepdog, HeadlessSheepdog
from scrapegoat_loom import Loom

def main():
    """
    """
    # SHEPHERD EXAMPLE
    shepherd = Shepherd(sheepdog=HeadlessSheepdog())
    shepherd.herd("example.goat")

    # LOOM EXAMPLE
    # html = Sheepdog().fetch("https://en.wikipedia.org/wiki/Web_scraping")
    # root = Gardener().grow_tree(html)
    # Loom(root).weave()


if __name__ == "__main__":
    main()
