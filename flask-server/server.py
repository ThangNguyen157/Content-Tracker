from flask import Flask, request, jsonify
from flask_cors import CORS
from scrape import Scrape

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
    
    html, style, css = spider.getModifiedHTMLCSS(content)
    with open("../client/src/viewpage.html", 'w', encoding="utf-8") as file:
        file.write(html)
    return {"value": html, 'css':css, 'style':style}

@app.route("/tags", methods=['POST'])
def tags():
    data = request.get_json()
    with open("../client/src/viewpage.html", 'w', encoding="utf-8") as file:
        file.write('')
    print(data)
    return {}
if __name__ == "__main__":
    app.run(debug=True)