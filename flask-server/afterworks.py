from scrape import Scrape
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv
import datetime
import time

def getSleepTime(cur):
    cur.execute('''SELECT * FROM data ORDER BY next_run ASC LIMIT 1''')
    dataDB = cur.fetchone()
    notTimeZoneAware = datetime.datetime.now(tz=datetime.UTC)
    diff = dataDB[4] - notTimeZoneAware
    return diff.total_seconds(), dataDB

def checkContent(cur, dataDB):
    newValue = []
    oldValue = []
    data = Scrape(dataDB[0])
    content = data.scrape()
    soup = data.getModifiedHTML(content)
    for index, id in enumerate(data[5]):
        minisoup = BeautifulSoup(data[6][index], 'html.parser')
        tag = soup.find(id=id)
        if (tag.get_text() != minisoup.get_text()):
            oldValue.append(tag.get_text())
            newValue.append(minisoup.get_text())
    return newValue, oldValue

def main():
    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                            password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    cur = conn.cursor()

    while True:
        seconds, dataDB = getSleepTime(cur)
        if (seconds > 4):
            break
        oldValue, newValue = checkContent(cur, dataDB)

        cur.execute()
        
    
    conn.commit()
    conn.close()
    cur.close()
    time.sleep(seconds)


if __name__ == "__main__":
    main()