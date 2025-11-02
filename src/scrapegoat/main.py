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
    """
    
    results = shepherd.herd(query)
    print(results)


if __name__ == "__main__":
    main()
