from scrape import Scrape
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv
import datetime
from datetime import timedelta
import time
import copy

def getSleepTime(conn, cur):
    cur.execute('''SELECT * FROM data ORDER BY next_run ASC LIMIT 1''')
    conn.commit()
    dataDB = cur.fetchone()
    notTimeZoneAware = datetime.datetime.now(tz=datetime.UTC)
    diff = dataDB[4] - notTimeZoneAware
    return diff.total_seconds(), dataDB

def checkContent(cur, dataDB):
    newValue = []
    oldValue = []
    changeType = []
    data = Scrape(dataDB[0])
    content = data.scrape()
    soup = data.getModifiedHTML(content)
    for index, id in enumerate(data[5]):
        minisoup = BeautifulSoup(data[6][index], 'html.parser')
        tag = soup.find(id=id)
        if (tag.get_text() != minisoup.get_text()):
            oldValue.append(tag)
            newValue.append(minisoup)
    return newValue, oldValue

def updateDB(conn, cur, dataDB, newValue=[]):
    #list is mutable so need to make a copy to avoid changing the original list
    nv = copy.copy(newValue)
    notTimeZoneAware = datetime.datetime.now(tz=datetime.UTC)
    newNext_run = notTimeZoneAware + timedelta(minutes=dataDB[2])
    for index, i in enumerate(dataDB[5]):
        if i not in nv:
            nv.insert(index, i)

    if not nv:
        cur.execute(f'''UPDATE data SET next_run = {newNext_run} WHERE data.time = {dataDB[3]}''')
    else:
        cur.execute(f'''UPDATE data SET next_run = {newNext_run}, tag = {nv} WHERE data.time = {dataDB[3]}''')
    conn.commit()

def main():
    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                            password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    cur = conn.cursor()

    while True:
        seconds, dataDB = getSleepTime(conn, cur)
        if (seconds > 4):
            break
        oldValue, newValue = checkContent(cur, dataDB)

        if newValue:
            updateDB(conn, cur, dataDB, newValue)
            #send email,....
            #check reply email,....
        else:
            updateDB(conn, cur, dataDB)

    
    
    conn.close()
    cur.close()
    time.sleep(seconds)


if __name__ == "__main__":
    main()