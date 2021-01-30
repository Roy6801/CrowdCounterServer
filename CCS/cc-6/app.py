from os import environ
from flask import Flask, render_template
from pyrebaseConnector.Connector import *
import threading

conn = Connection()
threading.Thread(target=conn.get_count).start()

app = Flask(__name__)

@app.route("/")
def home():
    return "Hi"

@app.route("/count")
def count():
    global conn
    return render_template("rough.html",dict=camDict)

if __name__ == "__main__":
	app.run(port=environ.get('PORT'),threaded=True)
