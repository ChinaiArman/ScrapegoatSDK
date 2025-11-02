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
    OUTPUT csv --filename "test1" --filepath "./outputs";
    VISIT "https://en.wikipedia.org/wiki/Dog";
    SCRAPE p;
    EXTRACT id, body;
    OUTPUT csv --filename "test2" --filepath "./outputs";
    """
    
    shepherd.herd(query)


if __name__ == "__main__":
    main()
