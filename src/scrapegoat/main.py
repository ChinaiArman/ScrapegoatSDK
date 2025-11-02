"""
"""

from scrapegoat import Shepherd


def main():
    """
    """
    shepherd = Shepherd()

    query = """
    VISIT "https://en.wikipedia.org/wiki/Web_scraping";
    SCRAPE p;
    EXTRACT id, body;
    OUTPUT csv --filename "test" --filepath "./outputs";
    SCRAPE a;
    EXTRACT id, body;
    OUTPUT json --filename "links" --filepath "./outputs";
    """
    
    shepherd.herd(query)


if __name__ == "__main__":
    main()
