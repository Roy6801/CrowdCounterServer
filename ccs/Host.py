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


app = Flask(__name__)
serverFile = open("cc-6/server.json","w")
camDict = dict()
host = dict()
started = list()

appName = input("\nEnter Remote App Name = ")
if appName.islower() != True:
    appName = appName.lower()
    print("\n\nRemote App Renamed to : "+appName)
os.system('heroku apps:destroy '+appName)


host['name'] = str(input("Enter server name = "))
host['ip'] = str(input("Enter Host ip = "))
host['port'] = int(input("Enter port number = "))
host['coverage'] = double(input("Enter area coverage for the server in sq. ft. (Default : 1 sq. ft.) = "))
if host['coverage'] < 1.0 :
    host['coverage'] = 1.0

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
    if camDict[cid].read() is None:
        del camDict[cid]


quality = int(input("Enter input quality parameter (allowed : 1 to 60, default : 15) = "))
if quality < 1 or quality > 60:
    host['quality'] = 480
else:
    host['quality'] = quality*32

json.dump(host, serverFile)
serverFile.close()
time.sleep(2.0)


@app.route("/")
def index():
    return render_template("CCC13.html")


@app.route("/<vid>")
def display(vid):
    if vid in camDict and vid not in started:
        started.append(vid)
        threading.Thread(target=detect, args=(vid, camDict[vid],host,)).start()
        return Response(capture(vid), mimetype="multipart/x-mixed-replace; boundary=frame")
    elif vid in camDict and vid in started:
        return Response(capture(vid), mimetype="multipart/x-mixed-replace; boundary=frame")
    else:
        return "<html><H1>No Connection " + vid + " Found!!</H1></html>"


def force_start():
    for i in camDict.keys():
        url = "http://"+host['ip']+":"+str(host['port'])+"/"+i
        try:
            urllib.request.urlopen(url)
        except:
            print("Trying to connect to : "+url)
    init_service()


def deploy():
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
    del_service()


def init_service():
    inp = input("\n\nEnter 'y' or 'Y' to deploy web service : ")
    if inp == "y" or inp == "Y":
        deploy()
    else:
        init_service()


def del_service():
    inp = input("\n\nEnter 'y' or 'Y' to shut down service : ")
    if inp == "y" or inp == "Y":
        os.system('heroku apps:destroy '+appName)
    else:
        del_service()

if __name__ == "__main__":
    threading.Timer(2.0,force_start).start()
    app.run(host=host['ip'], port=host['port'], debug=False, threaded=True, use_reloader=False)
