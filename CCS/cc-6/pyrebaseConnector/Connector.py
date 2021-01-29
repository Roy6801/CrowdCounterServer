import threading
import pyrebase
import json

serverFile = open("server.json","r")
pyrebaseFile = open("pyrebase.json","r")

host = json.load(serverFile)
firebaseConfig = json.load(pyrebaseFile)

serverFile.close()
pyrebaseFile.close()

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

class Connection:
    def __init__(self):
        self.camDict = dict()
        self.camList = list()

    def get_count(self):
        global db, host
        self.camList = db.child("Servers").child(host["name"]).child("Cameras").get()
        for i in self.camList.each():
            self.camDict[i.key()] = i.val()
        threading.Timer(0.5,self.get_count()).start()

    def get_total(self):
        self.total = 0
        for i in self.camDict:
            self.total = self.total + int(i)
        self.total_count = str(self.total)
        threading.Timer(0.5,self.get_total()).start()
