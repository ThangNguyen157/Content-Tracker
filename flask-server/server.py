from flask import Flask, request
from flask_cors import CORS
from scrape import Scrape
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import timedelta, timezone
import smtplib, datetime, os, psycopg2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
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

    #test given email
    message = MIMEMultipart()
    message["From"] = os.getenv('SENDER_EMAIL')
    message["To"] = data['clientEmail']
    message["Subject"] = 'Test Email'
    body = "This email is to verify that the given email is correct, and you can start receiving emails regarding content changes from now on."
    message.attach(MIMEText(body, "plain"))

    # Establish a connection to the SMTP server
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            # Start the TLS connection
            server.starttls()

            # Login to your Gmail account
            server.login(os.getenv('SENDER_EMAIL'), os.getenv('EMAIL_PASSWORD'))
            # Send the email
            server.sendmail(os.getenv('SENDER_EMAIL'), data['clientEmail'], message.as_string())
    except Exception as e:
        print('error sending email: '+ str(e))
        return {"value": 1}
    
    #start initial scraping
    spider = Scrape(data['link'])
    content = spider.scrape()
    if type(content) == int or content == "DNS address could not be found. Connection error." or content ==  'invalid url. Must start with https:// or http://' or content == 'invalid url.':
        print(content)
        return {"value":content}
    #get not timezone specific time
    notTimeZoneAware = datetime.datetime.now(tz=datetime.UTC)
    #turn not timezone aware object into naive 
    notTimeZoneAware2 = notTimeZoneAware.astimezone(timezone.utc).replace(tzinfo=None)
    newTime = notTimeZoneAware2 + timedelta(minutes=int(data['time']))

    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                        password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    cur = conn.cursor()

    cur.execute('''CREATE TABLE IF NOT EXISTS data (
                 url varchar(32779),
                 email varchar(320),
                 interval int,
                 time TIMESTAMP PRIMARY KEY,
                 next_run timestamp without time zone,
                 id text[],
                 tag text[])''')
    
    insertQuery ='''INSERT INTO data (url, email, interval, time, next_run) VALUES (%s, %s, %s, %s, %s)'''
    value = (data['link'], data['clientEmail'], data['time'], notTimeZoneAware2, newTime)
    #use place holder method to avoid SQL injecion
    cur.execute(insertQuery, value)
    conn.commit()
    conn.close()
    cur.close()

    html = spider.getModifiedHTML(content)
    htmlstr = str(html.prettify())
    with open("../client/src/viewpage.html", 'w', encoding="utf-8") as file:
        file.write(htmlstr)
    return {'value':htmlstr}

def getTagsByIDs(ids):
    with open('../client/src/viewpage.html','r') as f:
        data = f.read()

    soup = BeautifulSoup(data, "html.parser")
    tags = []
    for idd in ids:
        tags.append(str(soup.find(id=idd).parent))
    return tags

@app.route("/tags", methods=['POST'])
def tags():
    data = request.get_json()
    tags = getTagsByIDs(data['ids'])
    with open("../client/src/viewpage.html", 'w', encoding="utf-8") as file:
        file.write('')
    
    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                        password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    cur = conn.cursor()
    #select all row from the data table that is sorted in descending order by value in time column and then limit to 1 row(first row)(row with highest time stamp value)
    #ORDER BY will not sort the table permanently
    updateQuery= '''
    WITH LastRow AS (
        SELECT *
        FROM data
        ORDER BY time DESC
        LIMIT 1
    )
    UPDATE data
    SET id = %s,
        tag = %s
    FROM LastRow
    WHERE data.time = LastRow.time
'''
    value = (data['ids'], tags)
    cur.execute(updateQuery, value)
    conn.commit()
    conn.close()
    cur.close()

    return {}

@app.route("/unregister", methods=['POST'])
def unregister():
    data = request.get_json()

    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                        password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    cur = conn.cursor()
    query = '''DELETE FROM data WHERE email = %s'''
    value=[data['clientEmail']]
    cur.execute(query, value)
    conn.commit()
    #cur.rowcount return the number of row affected by the last query
    if not cur.rowcount:
        conn.close()
        cur.close()
        return {'value':"Email does not exist in the database. Please check the entered email."}
    else:
        conn.close()
        cur.close()
        return {'value':"Unregisted successfully"}
    

if __name__ == "__main__":
    app.run(debug=True)