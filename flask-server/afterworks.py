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

def checkContent(dataDB):
    newValue = []
    oldValue = []
    changeType = []
    newTag = []
    oldTag = []
    #if can not scrape
    data = Scrape(dataDB[0])
    content = data.scrape()
    soup = data.getModifiedHTML(content)

    #find change in text
    for index, id in enumerate(data[5]):
        minisoup = BeautifulSoup(data[6][index], 'html.parser')
        minisoup.find(id=id).unwrap()
        tag = soup.find(id=id)
        parent = tag.parent
        parent.span.unwrap()
        if len(newValue < index+1):
                oldTag.append([])
                newTag.append([])
                oldValue.append([])
                newValue.append([])
                changeType.append([])
        if parent.get_text() != minisoup.get_text():
            oldTag[index].append(str(minisoup.prettify()))
            newTag[index].append(str(parent.prettify()))
            oldValue[index].append(str(minisoup.get_text()))
            newValue[index].append(str(parent.get_text()))
            changeType[index].append('Change in content')
        if parent.name != minisoup.name:
            oldTag[index].append(str(minisoup.prettify()))
            newTag[index].append(str(parent.prettify()))
            oldValue[index].append(str(minisoup.name))
            newValue[index].append(str(parent.name))
            changeType[index].append('Change in tag name')
        
        if len(parent.attrs) > len(minisoup.attrs):
            big = parent.attrs
            small = minisoup.attrs
        else:
            big = minisoup.atrrs
            small = parent.attrs
        for key in (list(big.keys())):
            if key not in list(small.keys()):
                oldTag[index].append(str(minisoup.prettify()))
                newTag[index].append(str(parent.prettify()))
                oldValue[index].append('not having that attribute before or it was removed')
                newValue[index].append(key+ ' = '+ big['key'])
                changeType[index].append('new attribute added/removed')
            elif minisoup.attrs[key] != parent.attrs[key]:
                oldTag[index].append(str(minisoup.prettify()))
                newTag[index].append(str(parent.prettify()))
                oldValue[index].append(minisoup.attrs[key])
                newValue[index].append(parent.attrs[key])
                changeType[index].append("Change in attribute's value")
        if not newTag[-1]:
            oldTag.pop()
            newTag.pop()
            oldValue.pop()
            newValue.pop()
            changeType.pop()

    return newTag, oldTag, newValue, oldValue, changeType

def updateDB(conn, cur, dataDB, newTag=[]):
    #list is mutable so need to make a copy to avoid changing the original list
    nv = copy.copy(newTag)

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
        oldTag, newTag, newValue, oldValue, changeType = checkContent(dataDB)

        if newTag:
            updateDB(conn, cur, dataDB, newTag)
            #send email,....
            #check reply email,....
        else:
            updateDB(conn, cur, dataDB)
    
    conn.close()
    cur.close()
    time.sleep(seconds)


if __name__ == "__main__":
    main()