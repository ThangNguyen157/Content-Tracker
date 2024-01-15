from scrape import Scrape
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv
import datetime
import time

def getSleepTime(conn, cur):
    cur.execute('''SELECT * FROM data ORDER BY next_run ASC LIMIT 1;"''')
    time = cur.fetchone()[0]
    notTimeZoneAware = datetime.datetime.now(tz=datetime.UTC)
    diff = time - notTimeZoneAware
    return diff.total_seconds()


def main():
    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                            password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    cur = conn.cursor()

    while True:
        
        cur.execute()
        seconds = getSleepTime(conn, cur)
        if (seconds > 4):
            break
    
    conn.commit()
    conn.close()
    cur.close()
    time.sleep(seconds)


if __name__ == "__main__":
    main()