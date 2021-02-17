from myUtils.dataProcessor.Processor import process_time
from matplotlib import pyplot as plt
import pyrebase
import threading
import json
import time
import os

pyrebaseFile = open("cc-6/pyrebase.json","r")
firebaseConfig = json.load(pyrebaseFile)
pyrebaseFile.close()
serverFile = open("cc-6/server.json","r")
host = json.load(serverFile)
serverFile.close()

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

plots = dict()

counter = 0

def plotter():
    global db, storage, plots
    file = str(int(time.time()))
    temp = []
    plt.clf()
    for i in plots:
        temp.append(process_time(i))
    plt.plot(temp,plots.values())
    plt.xlabel('Time', fontsize=18)
    plt.ylabel('Count', fontsize=20)
    fig = plt.gcf()
    fig.suptitle('Crowd Count vs Time ('+host["name"]+")", fontsize=28)
    fig.set_size_inches(18.5, 10.5)
    fig.savefig(host["name"]+"_plot.jpg")
    storage.child(host["name"]).child(file+".jpg").put(host["name"]+"_plot.jpg")
    url = storage.child(host["name"]).child(file+".jpg").get_url(None)
    db.child("History").child(host["name"]).child(file).set(url)


def modify_plots():
    timestamp = int(time.time())
    if timestamp % 10 == 0:
        threading.Thread(target=record,args=(timestamp,)).start()
    threading.Thread(target=modify_plots).start()


def record(ts):
    global db, counter, plots, host
    total = db.child("Hosts").child(host["name"]).get()
    if total.val() is not None:
        total = float(total.val()) * host["coverage"]
        plots[int(ts)] = int(round(total))
        counter = counter + 1
    if counter == 5:
        counter = 0
    erase(ts)


def erase(ts):
    global plots
    temp = list()
    for i in plots:
        if i < (ts - 50):
            temp.append(i)
    for j in temp:
        del plots[j]


modify_plots()
while True:
    if int(time.time()) % 30 == 0:
        plotter()
