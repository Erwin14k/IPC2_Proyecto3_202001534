from flask import Flask
from flask_cors import CORS
from flask.globals import request
app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return "<h1>Ruta Principal 14k</h1>"



if __name__ == "__main__":
    app.run(threaded=True, port=5000,debug=True)
