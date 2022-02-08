import requests
import pandas as pd
from bs4 import BeautifulSoup

class Scraper:
    """
    Scraper Class: It handles the main functionality of scraping data in form of tables from the given url
    """
    def __repr__(self):
        """
        Representation of scraper class is defined here.
        The representation is show when an object of the class is printed.
        """
        return "Scraper Class"

    def scrape_table(self, url):
        """
        This function scrapes a table from the given url and returns it as a Pandas DataFrame.
        Beautiful Soup and Requests libraries are used for scraping the table.
        Pandas is used for storing the table as a DataFrame (table).

        Parameters:
        - URL: A String containing url of website to scrape.
        """
        soup = BeautifulSoup(requests.get(url).text, features="html.parser")
        headers = [header.text for listing in soup.find_all('thead') for header in listing.find_all('th')]
        raw_data = {header:[] for header in headers}

        for rows in soup.find_all('tbody'):
            for row in rows.find_all('tr'):
                if len(row) != len(headers): continue
                for idx, cell in enumerate(row.find_all('td')):
                    raw_data[headers[idx]].append(cell.text)

        return pd.DataFrame(raw_data)[:90]

if __name__ == '__main__':
    scr = Scraper()
    print("\nTop 250 IMDB Movies:")
    print(scr.scrape_table("https://www.imdb.com/chart/top/"))