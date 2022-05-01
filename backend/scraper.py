import time
import lxml
import re
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver

opts = webdriver.ChromeOptions()
opts.headless = True
driver = webdriver.Chrome(options=opts)

class Scraper:
    """
    The Main Scraper Class which scrapes info from imdb url
    """
    url = ["https://www.imdb.com/search/title/?title_type=feature,tv_series&count=250",
"https://www.imdb.com/search/title/?title_type=feature&count=250",
"https://www.imdb.com/search/title/?title_type=tv_series&count=250"]
    thumbtail= "UX67_CR0,0,67,98_AL_.jpg"
    thumbtail2= "UY98_CR0,0,67,98_AL_.jpg"

    def __repr__(self):
        """
        Representation of Scraper class is defined here.
        The representation is shown when an object of the class is printed.
        """
        return "Scraper Class"

    def __init__(self, url):
        super(Scraper, self).__init__()
        if url != 'true':
            driver.get(url)
            y = 700
            for timer in range(0,70):
                driver.execute_script("window.scrollTo(0, "+str(y)+")")
                y += 700
                time.sleep(1)
            self.soup = BeautifulSoup(driver.page_source, 'lxml')

    def articleTitle(self):
        return self.soup.find("h1", class_="header").text.replace("\n","")

    def bodyContent(self):
        content = self.soup.find(id="main")
        return content.find_all("div", class_="lister-item mode-advanced")

    def mediaData(self):
        mediaFrame = self.bodyContent()
        mediaTitle = []
        mediaDate = []
        mediaRunTime = []
        mediaGenre = []
        mediaRating = []
        mediaScore = []
        mediaDescription = []
        mediaDirector = []
        mediaStars = []
        mediaVotes = []
        mediaThumbnail = []
        for media in mediaFrame:
            mediaFirstLine = media.find("h3", class_="lister-item-header")
            mediaTitle.append(mediaFirstLine.find("a").text)
            mediaDate.append(re.sub(r"[()]","", mediaFirstLine.find_all("span")[-1].text))
            try:
                mediaRunTime.append(media.find("span", class_="runtime").text[:-4])
            except:
                mediaRunTime.append(np.nan)
            mediaGenre.append(media.find("span", class_="genre").text.rstrip().replace("\n","").split(","))
            try:
                mediaRating.append(media.find("strong").text)
            except:
                mediaRating.append(np.nan)
            try:
                mediaScore.append(media.find("span", class_="metascore unfavorable").text.rstrip())
            except:
                mediaScore.append(np.nan)
            mediaDescription.append(media.find_all("p", class_="text-muted")[-1].text.lstrip())
            mediaCast = media.find("p", class_="")

            thumb = media.find("div", class_="lister-item-image float-left")
            thumb2 = thumb.find("a")
            mediaThumbnail.append(thumb2.find("img").get("src").split('._V1_')[0]+'._V1_')

            try:
                casts = mediaCast.text.replace("\n","").split('|')
                casts = [x.strip() for x in casts]
                casts = [casts[i].replace(j, "") for i,j in enumerate(["Director:", "Stars:"])]
                mediaDirector.append(casts[0])
                mediaStars.append([x.strip() for x in casts[1].split(",")])
            except:
                casts = mediaCast.text.replace("\n","").strip()
                mediaDirector.append(np.nan)
                mediaStars.append([x.strip() for x in casts.split(",")])

            mediaNumbers = media.find_all("span", attrs={"name": "nv"})

            if len(mediaNumbers) == 2:
                mediaVotes.append(mediaNumbers[0].text)
            elif len(mediaNumbers) == 1:
                mediaVotes.append(mediaNumbers[0].text)
            else:
                mediaVotes.append(np.nan)

        media_info = [mediaTitle, mediaDate, mediaGenre, mediaRating, mediaScore, mediaDescription,
                        mediaDirector, mediaStars, mediaVotes, mediaRunTime, mediaThumbnail]
        media_info_df = pd.DataFrame(media_info)
        media_info_df = media_info_df.transpose()
        media_info_df.columns = ['Title', 'Date', 'Genre', 'Rating', 'Score', 'Description', 'Director', 'Stars', 'Votes', 'Runtime', 'Thumbnail']
        return media_info_df

    def main(self):
        i = 1
        for url in self.url:
            self.__init__(url)
            media_info = Scraper.mediaData(self)
            if i == 1:
                media_info.to_json("db/media.json")
                i+=1
            elif i == 2:
                media_info.to_json("db/movies.json")
                i+=1
            elif i == 3:
                media_info.to_json("db/shows.json")
                i = 1
            
if __name__ == '__main__':
    scr = Scraper('true')
    scr.main()