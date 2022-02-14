from bs4 import BeautifulSoup
import requests
import re
 
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
        # Downloading imdb top 250 movie's data
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        
        movies = soup.select('td.titleColumn')
        links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
        crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        
        ratings = [b.attrs.get('data-value')
                for b in soup.select('td.posterColumn span[name=ir]')]
        
        votes = [b.attrs.get('data-value')
                for b in soup.select('td.ratingColumn strong')]
        
        list = []
        
        # create a empty list for storing
        # movie information
        list = []
        
        # Iterating over movies to extract
        # each movie's details
        for index in range(0, len(movies)):
            
            # Separating  movie into: 'place',
            # 'title', 'year'
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index))+1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index))-(len(movie))]
            data = {"movie_title": movie_title,
                    "year": year,
                    "place": place,
                    "star_cast": crew[index],
                    "rating": ratings[index],
                    "vote": votes[index],
                    "link": links[index]}
            list.append(data)
        
        # printing movie details with its rating.
        for movie in list:
            print(movie['place'], '-', movie['movie_title'], '('+movie['year'] +
                ') -', 'Starring:', movie['star_cast'], movie['rating'])

if __name__ == '__main__':
    url = 'http://www.imdb.com/chart/top'
    scr = Scraper();
    scr.scrape_table(url)
