"""
"""

from scrapegoat import Shepherd, Sheepdog, Loom


def main():
    """
    """
    sheepdog = Sheepdog()

    html = sheepdog.fetch("https://en.wikipedia.org/wiki/Web_scraping")
    
    shepherd = Shepherd()
    root = shepherd.sow(html)

    query = "SCRAPE ALL h2 IN POSITION=4;" # A simple Goatspeak query to scrape all h2 elements
    results = shepherd.lead_goat(root, query) # Execute the query against the HTML tree

    for result in results:
        print(result)


if __name__ == "__main__":
    main()
