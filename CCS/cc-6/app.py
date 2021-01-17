from os import environ
from flask import Flask, render_template
from pyrebaseConnector.Connector import *
import threading

conn = Connection()
threading.Thread(target=conn.get_count).start()

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/count")
def count():
    global conn
    return "Hi"

if __name__ == "__main__":
	app.run(port=environ.get('PORT'),threaded=True)
