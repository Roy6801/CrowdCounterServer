import pyrebase
import threading
import time
import json
import os

pyrebaseFile = open("cc-6/pyrebase.json","r")
firebaseConfig = json.load(pyrebaseFile)
pyrebaseFile.close()

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

def set_app(host,name):
    global db
    db.child("Servers").child(host["name"]).child("app").set(name)
    db.child("Servers").child(host["name"]).child("appURL").set("https://"+name+".herokuapp.com")


class Connection:
    def __init__(self, cid, host):
        global db
        self.count = ""
        self.cid = cid
        self.host = host
        db.child("Servers").child(self.host["name"]).set(self.host)
        threading.Thread(target=self.update_count).start()

    def set_count(self, count):
        self.count = count

    def update_count(self):
        global db
        db.child("Servers").child(self.host["name"]).child("Cameras").child(self.cid).set(str(self.count))
        threading.Timer(0.5, self.update_count).start()
        timestamp = int(time.time())
        if timestamp % 300 == 0:
            threading.Thread(target=self.record,args=(timestamp,)).start()

    def record(self, ts):
        global db
        db.child("History").child(ts).child("Servers").child(self.host["name"]).child("Cameras").child(self.cid).set(str(self.count))
        self.erase(ts)

    def erase(self, ts):
        global db
        history = db.child("History").get()
        for i in history:
            if int(i.key()) < (ts - host["memory"]*86400):
                db.child("History").child(i.key()).remove()
