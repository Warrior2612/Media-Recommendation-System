import backend.scraper
import backend.recommendation
from flask_website import app as web_app

from datetime import datetime
import time
import threading

def updateDB(lastUpdateTime=datetime.utcnow()):
    while(True):
        time.sleep(11)
        now = datetime.utcnow()
        if (now - lastUpdateTime).total_seconds() > 10:
            print(f'{lastUpdateTime:%H:%M:%S%z}'+" Updating DB")
            scr = backend.scraper.Scraper()
            scr.main()
            lastUpdateTime = datetime.utcnow()
            print(f'{lastUpdateTime:%H:%M:%S%z}'+" DB succesfully updated!")
        else:
            time.sleep(5)

def flask_app():
    web_app.run()

def main():
    t1 = threading.Thread(target=flask_app)
    t2 = threading.Thread(target=updateDB)

    t1.start()
    t2.start()

if __name__ == '__main__':
    main()