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
counter = 0


def set_app(host,name):
    global db
    db.child("Servers").child(host["name"]).child("app").set(name)
    db.child("Servers").child(host["name"]).child("appURL").set("https://"+name+".herokuapp.com")


class Connection:
    def __init__(self, cid, host):
        global db
        self.plots = dict()
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
        threading.Thread(target=self.update_count).start()
        timestamp = int(time.time())
        if timestamp % 10 == 0:
            threading.Thread(target=self.record,args=(timestamp,)).start()

    def record(self, ts):
        global db, counter
        total = db.child("Hosts").child(self.host["name"]).get()
        if total.val() is not None:
            self.plots[int(ts)] = int(total.val())
            counter = counter + 1
        if counter == 6:
            with open(self.host["name"]+".json","w") as file:
                json.dump(self.plots,file)
            counter = 0
        self.erase(ts)

    def erase(self, ts):
        temp = list()
        for i in self.plots:
            if i < (ts - 50):
                temp.append(i)
        for j in temp:
            del self.plots[j]
