from myUtils.dataProcessor.Processor import process_time
from matplotlib import pyplot as plt
import pyrebase
import threading
import json
import time

pyrebaseFile = open("cc-6/pyrebase.json","r")
firebaseConfig = json.load(pyrebaseFile)
pyrebaseFile.close()

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

mall_plt = dict()

count = 0
counter = 0

def mall_area(area):
    global db
    db.child("Mall").child("area").set(str(area))

def mall_count(area):
    global db, count
    total = 0
    servers = db.child("Hosts").get()
    serverCount = len(servers.val())
    for i in servers:
        total = total + float(i.val())
    count = int(round((float(area)*total)/serverCount))
    db.child("Mall").child("count").set(str(count))
    threading.Thread(target=mall_count,args=(area,)).start()

def mall_plot():
    global db, storage, mall_plt
    file = str(int(time.time()))
    temp = []
    plt.clf()
    for i in mall_plt:
        temp.append(process_time(i))
    plt.plot(temp,mall_plt.values())
    plt.xlabel('Time', fontsize=18)
    plt.ylabel('Count', fontsize=20)
    fig = plt.gcf()
    fig.suptitle('Crowd Count vs Time (Mall)', fontsize=28)
    fig.set_size_inches(18.5, 10.5)
    fig.savefig("Mall_plot.jpg")
    storage.child("Mall").child(file+".jpg").put("Mall_plot.jpg")
    url = storage.child("Mall").child(file+".jpg").get_url(None)
    db.child("Mall").child("History").child(file).set(url)

def modify_mall_plt():
    timestamp = int(time.time())
    if timestamp % 10 == 0:
        threading.Thread(target=record,args=(timestamp,)).start()
    threading.Thread(target=modify_mall_plt).start()


def record(ts):
    global db, counter, mall_plt, count
    mall_plt[int(ts)] = count
    counter = counter + 1
    if counter == 5:
        counter = 0
    erase(ts)


def erase(ts):
    global mall_plt
    temp = list()
    for i in mall_plt:
        if i < (ts - 50):
            temp.append(i)
    for j in temp:
        del mall_plt[j]

area = input("Enter total mall area in sq. m. = ")
mall_area(area)
mall_count(area)
modify_mall_plt()
while True:
    if int(time.time()) % 30 == 0:
        mall_plot()
