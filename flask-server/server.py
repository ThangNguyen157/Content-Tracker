from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape import Scrape
from bs4 import BeautifulSoup
import psycopg2
import os
from dotenv import load_dotenv
import datetime
from datetime import timezone, timedelta
#import geocoder
#from timezonefinder import TimezoneFinder

app = Flask(__name__)
CORS(app)

@app.route("/data", methods=['POST'])
def data():
    #force=True to skip content type requirement
    data = request.get_json()

    #handle timezone specific to user
    '''
    # Get the user's IP address from the request
    user_ip = request.remote_addr
    #will not work on local host since the ip address is a loop back ip address. Can not find lattitude and longtitude from it 
    info = geocoder.ipinfo(user_ip)
    # Use timezonefinder to get the timezone based on the location
    tf = TimezoneFinder()
    timezone_str = tf.timezone_at(lng=info.latlng[1], lat=info.latlng[0])
    print(timezone_str)'''

    spider = Scrape(data['link'])
    content = spider.scrape()

    if type(content) == int or content == "DNS address could not be found":
        return {"value":content}
    #get not timezone specific time
    notTimeZoneAware = datetime.datetime.now(tz=datetime.UTC)
    newTime = notTimeZoneAware + timedelta(minutes=int(data['time']))

    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                        password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    curr = conn.cursor()

    curr.execute('''CREATE TABLE IF NOT EXISTS data (
                 url varchar(32779),
                 email varchar(320),
                 interval int,
                 time TIMESTAMP,
                 next_run timestamp without time zone,
                 id integer[],
                 tag varchar(50000))''')
    insertQuery ='''INSERT INTO data (url, email, interval, time, next_run) VALUES (%s, %s, %s, %s, %s)'''
    value = (data['link'], data['clientEmail'], data['time'], notTimeZoneAware, newTime)
    #use place holder method to avoid SQL injecion
    curr.execute(insertQuery, value)
    conn.commit()
    conn.close()
    curr.close()
    html = spider.getModifiedHTMLCSS(content)
    with open("../client/src/viewpage.html", 'w', encoding="utf-8") as file:
        file.write(html)
    return {'value':html}

def getTagsByIDs(ids):
    with open('../client/src/viewpage.html','r') as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")
    tags = []
    for idd in ids:
        tags.append(soup.find(id=idd).parent)
    return tags

@app.route("/tags", methods=['POST'])
def tags():
    data = request.get_json()
    tags = getTagsByIDs(data['ids'])
    with open("../client/src/viewpage.html", 'w', encoding="utf-8") as file:
        file.write('')
    
    return {}
if __name__ == "__main__":
    app.run(debug=True)