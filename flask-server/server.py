from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
@app.route("/data", methods=['POST'])
def data():
    data = request.get_json()
    print(data)
    return jsonify({"d":"ddd"})

if __name__ == "__main__":
    app.run(debug=True)