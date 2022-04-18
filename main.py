import backend.scraper
import backend.dbConnector
import backend.recommendation

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

def algo():
    for i in range(9999999999):
        print(i)
        time.sleep(1)

def main():
    t1 = threading.Thread(target=updateDB)
    t2 = threading.Thread(target=algo)

    t1.start()
    t2.start()

if __name__ == '__main__':
    main()