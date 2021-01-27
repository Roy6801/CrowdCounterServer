from myUtils.yoloDetector.Detector import *
from myUtils.pyrebaseConnector.Connector import set_app
from imutils.video import VideoStream
from flask import Flask, Response, render_template
from git import rmtree
import urllib
import threading
import time
import json
import os

o
app = Flask(__name__)
serverFile = open("cc-6/server.json","w")
camDict = dict()
host = dict()
started = list()


os.system('heroku login -i')
appName = input("\nEnter Remote App Name = ")
if appName.islower() != True:
    appName = appName.lower()
    print("\n\nRemote App Renamed to : "+appName)
os.system('heroku apps:destroy '+appName)

while True:
    tempId = input("Enter cam number = ")
    if tempId == "-1":
        break
    flr = input("Enter floor number = ")
    shp = input("Enter shop number = ")
    cam = input("Enter cam address = ")
    try:
        cam = int(cam)
    except:
        cam = str(cam)
    capt = VideoStream(src=cam).start()
    cid = "f"+flr+"s"+shp+"c"+tempId
    camDict[cid] = capt

host['ip'] = str(input("Enter Host ip = "))
host['port'] = int(input("Enter port number = "))
host['name'] = str(input("Enter server name = "))
json.dump(host, serverFile)
serverFile.close()
time.sleep(2.0)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/<vid>")
def display(vid):
    global host, camDict
    if vid in camDict and vid not in started:
        started.append(vid)
        threading.Thread(target=detect, args=(vid, camDict[vid],host,)).start()
        return Response(capture(vid), mimetype="multipart/x-mixed-replace; boundary=frame")
    elif vid in camDict and vid in started:
        return Response(capture(vid), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        return "No Connection " + vid + " Found!!"


def force_start():
    global camDict, started, host
    time.sleep(5.0)
    for i in camDict.keys():
        url = "http://"+host['ip']+":"+str(host['port'])+"/"+i
        urllib.request.urlopen(url)
    deploy(host)

def deploy(host):
    global appName
    print("\n\n********** Deploying to Web **********")
    os.chdir(os.getcwd()+"/cc-6")
    os.system('git init')
    set_app(host,appName)
    os.system('heroku apps:create '+appName)
    os.system('git add .')
    os.system('git commit -m "Deployed to Web!"')
    os.system('heroku buildpacks:set heroku/python')
    try:
        os.system('git push heroku master')
    except:
        print("\n\nTry another name!!!")
        return deploy(host)
    os.system('heroku open')
    rmtree(os.getcwd()+"/.git")
    print("\n\n********** Server Online **********")
    print("\n\n##### Do not kill this Process ####")
    shut()

def shut():
    inp = input("\n\nEnter 'y' or 'Y' to close server : ")
    if inp == "y" or inp == "Y":
        os.system('heroku apps:destroy '+appName)
    else:
        shut()

if __name__ == "__main__":
    threading.Thread(target=force_start).start()
    app.run(host=host['ip'], port=host['port'], debug=False, threaded=True, use_reloader=False)
