"""
"""

from scrapegoat import Shepherd, Sheepdog


def main():
    """
    """
    sheepdog = Sheepdog()

    html = sheepdog.fetch("https://en.wikipedia.org/wiki/Web_scraping")
    
    shepherd = Shepherd()
    root = shepherd.pasture(html)

    query = """
    SCRAPE 3 table;
    OUTPUT csv --filename "test" --filepath "./outputs";
    """
    results = shepherd.herd(root, query)

    # print([result.to_dict() for result in results])


if __name__ == "__main__":
    main()
