from bs4 import BeautifulSoup
import requests
import lxml
import re
import pandas as pd
import numpy as np
 
class movies_by_top250:
    """
    movies_by_top250 Class: It handles the main functionality of scraping data in form of tables from the given url
    """
    def __repr__(self):
        """
        Representation of movies_by_top250 class is defined here.
        The representation is show when an object of the class is printed.
        """
        return "movies_by_top250 Class"

    def scrape_table(self, url):
        """
        This function scrapes a table from the given url and returns it as a Pandas DataFrame.
        Beautiful Soup and Requests libraries are used for scraping the table.
        Pandas is used for storing the table as a DataFrame (table).

        Parameters:
        - URL: A String containing url of website to scrape.
        """
        # Downloading movies_by_genre top 250 movie's data
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
        
        # Iterating over movies to extract each movie's details
        for index in range(0, len(movies)):
            # Separating  movie into: 'place', 'title', 'year'
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

class movies_by_genre(object):
	"""docstring for movies_by_genre"""
	def __init__(self, url):
		super(movies_by_genre, self).__init__()
		page = requests.get(url)

		self.soup = BeautifulSoup(page.content, 'lxml')

	def articleTitle(self):
		return self.soup.find("h1", class_="header").text.replace("\n","")

	def bodyContent(self):
		content = self.soup.find(id="main")
		return content.find_all("div", class_="lister-item mode-advanced")

	def movieData(self):
		movieFrame = self.bodyContent()
		movieTitle = []
		movieDate = []
		movieRunTime = []
		movieGenre = []
		movieRating = []
		movieScore = []
		movieDescription = []
		movieDirector = []
		movieStars = []
		movieVotes = []
		movieGross = []
		for movie in movieFrame:
			movieFirstLine = movie.find("h3", class_="lister-item-header")
			movieTitle.append(movieFirstLine.find("a").text)
			movieDate.append(re.sub(r"[()]","", movieFirstLine.find_all("span")[-1].text))
			try:
				movieRunTime.append(movie.find("span", class_="runtime").text[:-4])
			except:
				movieRunTime.append(np.nan)
			movieGenre.append(movie.find("span", class_="genre").text.rstrip().replace("\n","").split(","))
			try:
				movieRating.append(movie.find("strong").text)
			except:
				movieRating.append(np.nan)
			try:
				movieScore.append(movie.find("span", class_="metascore unfavorable").text.rstrip())
			except:
				movieScore.append(np.nan)
			movieDescription.append(movie.find_all("p", class_="text-muted")[-1].text.lstrip())
			movieCast = movie.find("p", class_="")

			try:
				casts = movieCast.text.replace("\n","").split('|')
				casts = [x.strip() for x in casts]
				casts = [casts[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
				movieDirector.append(casts[0])
				movieStars.append([x.strip() for x in casts[1].split(",")])
			except:
				casts = movieCast.text.replace("\n","").strip()
				movieDirector.append(np.nan)
				movieStars.append([x.strip() for x in casts.split(",")])

			movieNumbers = movie.find_all("span", attrs={"name": "nv"})

			if len(movieNumbers) == 2:
				movieVotes.append(movieNumbers[0].text)
				movieGross.append(movieNumbers[1].text)
			elif len(movieNumbers) == 1:
				movieVotes.append(movieNumbers[0].text)
				movieGross.append(np.nan)
			else:
				movieVotes.append(np.nan)
				movieGross.append(np.nan)

		movie_info = [movieTitle, movieDate, movieRunTime, movieGenre, movieRating, movieScore, movieDescription,
							movieDirector, movieStars, movieVotes, movieGross]
		return movie_info
	
	def main(self):
		movie_info = movies_by_genre.movieData(self)
		print(movie_info[0])

if __name__ == '__main__':
	url = 'http://www.movies_by_genre.com/chart/top'
	url2 = 'https://www.movies_by_genre.com/search/title/?title_type=feature&num_votes=25000,&genres=action'
	scr = movies_by_top250();
	scr.scrape_table(url)
	print("\n")
	id1 = movies_by_genre(url2)
	print(id1.articleTitle())
	id1.main();