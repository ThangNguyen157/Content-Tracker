from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape import Scrape
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

@app.route("/data", methods=['POST'])
def data():
    #force=True to skip content type requirement
    data = request.get_json()
    spider = Scrape(data['link'], data['time'], data['clientEmail'])
    content = spider.scrape()

    if type(content) == int or content == "DNS address could not be found":
        return {"value":content}
    
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