from scrape import Scrape
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import timedelta
import time, copy, smtplib, os, psycopg2, datetime, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

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

def sendEmail(oldTag, newTag, newValue, oldValue, changeType, email, url):
    message = MIMEMultipart()
    message["From"] = os.getenv('SENDER_EMAIL')
    message["To"] = email
    message["Subject"] = 'Change(s) Detected'
    HTML = f'''
            <html>
            <head>
            </head>
            <body>
            <p>New change(s) detected at<a href={url}>the website</a> you provided</p>
            <p style='text-align:center'>
                <table>
                    <thead>
                        <tr>
                            <th>Change Type</th>
                            <th>Old Value</th>
                            <th>New Value</th>
                            <th>Old tag</th>
                            <th>New tag</th>
                        </tr>
                    </thead>
                </table>
            </p>
            <p style='text-align: center; font-weight:bold; font-size:20px'>To stop receving email, please visit <a href="content-tracker.com">content-tracker.com</a> and enter your email at the bottom field.</p>
            </body>
            </html>
        '''
    soup = BeautifulSoup(HTML, 'html.parser')
    table = soup.find('table')
    for l in oldTag:
        new_row = soup.new_tag('tr')
        td1 = soup.new_tag('td')
        td1.string = changeType[i]
        td2 = soup.new_tag('td')
        td2.string = oldValue[i]
        td3 = soup.new_tag('td')
        td3.string = newValue[i]
        td4 = soup.new_tag('td', rowspan=str(i))
        td4.string = oldTag[i]
        td5 = soup.new_tag('td', rowspan=str(i))
        td5.string = newTag[i]
        new_row.append(td1)
        new_row.append(td2)
        new_row.append(td3)
        new_row.append(td4)
        new_row.append(td5)
        table.append(new_row)
        for i in len(1, l):
            new_row = soup.new_tag('tr')
            td1 = soup.new_tag('td')
            td1.string = changeType[i]
            td2 = soup.new_tag('td')
            td2.string = oldValue[i]
            td3 = soup.new_tag('td')
            td3.string = newValue[i]
            new_row.append(td1)
            new_row.append(td2)
            new_row.append(td3)
            table.append(new_row)
    # Attach the HTML content
    message.attach(MIMEText(HTML, "html"))

    # Establish a connection to the SMTP server
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            # Start the TLS connection
            server.starttls()

            # Login to your Gmail account
            server.login(os.getenv('SENDER_EMAIL'), os.getenv('EMAIL_PASSWORD'))
            # Send the email
            server.sendmail(os.getenv('SENDER_EMAIL'), email, message.as_string())
    except Exception as e:
        print('error sending email: '+ str(e))
        return 0
    return 1


def main():
    load_dotenv()
    conn = psycopg2.connect(host=os.getenv('HOST'), dbname=os.getenv('DBNAME'), user=os.getenv('USER'), 
                            password=os.getenv('PASSWORD'), port=os.getenv('PORT'))
    cur = conn.cursor()

    while True:
        cur.execute('''DELETE FROM data WHERE id IS NULL''')
        cur.execute('''SELECT COUNT(*) FROM data''')
        conn.commit()
        if not cur.fetchone()[0]:
            seconds = 6000
            break
        seconds, dataDB = getSleepTime(conn, cur)
        if (seconds > 5):
            break
        oldTag, newTag, newValue, oldValue, changeType = checkContent(dataDB)

        if newTag:
            updateDB(conn, cur, dataDB, newTag)
            if not sendEmail(oldTag, newTag, newValue, oldValue, changeType, dataDB[1], dataDB[0]):
                cur.execute(f'''DELETE FROM data WHERE time = {dataDB[3]}''')
                conn.commit()
        else:
            updateDB(conn, cur, dataDB)
    
    conn.close()
    cur.close()
    time.sleep(seconds)


if __name__ == "__main__":
    main()