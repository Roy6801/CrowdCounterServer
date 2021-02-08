from css.myUtils.dataProcessor.Processor import process_time
from matplotlib import pyplot as plt
import pyrebase
import json
import time

pyrebaseFile = open("ccs/cc-6/pyrebase.json","r")
firebaseConfig = json.load(pyrebaseFile)
pyrebaseFile.close()
serverFile = open("ccs/cc-6/server.json","r")
host = json.load(serverFile)
serverFile.close()


firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
storage = firebase.storage()

plots = dict()

def plotter():
    global db, storage, plots
    with open("ccs/"+host["name"]+".json","r") as file:
        plots = json.load(file)
    plt.clf()
    plt.plot(plots.keys(),plots.values())
    plt.savefig(host["name"]+"_plot.jpg")
    storage.child(host["name"]).child(str(int(time.time()))+".jpg").put(host["name"]+"_plot.jpg")


while True:
    plotter()
    time.sleep(30.0)
