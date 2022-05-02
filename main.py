import backend.scraper
import backend.recommendation
import flask_website

from datetime import datetime
import time
import threading

def updateDB(lastUpdateTime=datetime.utcnow()):
    scr = backend.scraper.Scraper('true')
    while(True):
        time.sleep(11)
        now = datetime.utcnow()
        if (now - lastUpdateTime).total_seconds() > 10:
            print(f'{lastUpdateTime:%H:%M:%S%z}'+" Updating DB")
            scr.main()
            lastUpdateTime = datetime.utcnow()
            print(f'{lastUpdateTime:%H:%M:%S%z}'+" DB succesfully updated!")
        else:
            time.sleep(5)

def flask_app():
    flask_website.app.run()

def recommender():
    time.sleep(5)
    while True:
        liked_ids = flask_website.liked_ids
        print(liked_ids)
        if len(liked_ids) != 0:
            for i in liked_ids:
                backend.recommendation.main(i)
            flask_website.recommended_ids = backend.recommendation.recommended_ids[::-1]
        print(backend.recommendation.recommended_ids)
        time.sleep(2)

def main():
    t1 = threading.Thread(target=flask_app)
    t2 = threading.Thread(target=updateDB)
    t3 = threading.Thread(target=recommender)

    t1.start()
    t2.start()
    t3.start()

if __name__ == '__main__':
    main()