from flask import Flask, render_template
from pyrebaseConnector.Connector import *
import threading
import json

conn = Connection()
threading.Thread(target=conn.get_count).start()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("CCC13.html")


@app.route("/count_path")
def count_path():
    global conn
    return json.dumps(conn.camDict)


@app.route("/count")
def count():
    global conn
    return render_template("index.html")

if __name__ == "__main__":
	app.run('0.0.0.0',threaded=True)
