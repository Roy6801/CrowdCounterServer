from myUtils.yoloDetector.Detector import *
from myUtils.pyrebaseConnector.Connector import set_app
from imutils.video import VideoStream
from flask import Flask, Response, render_template
import urllib
import threading
import time
import json
import os


app = Flask(__name__)
camDict = dict()
host = dict()
started = list()

loadFrom = input("\n\nLoad last saved server? (y/n) - ")

if not os.path.exists("cc-6/server.json") or loadFrom.lower() == "n":
    host['name'] = str(input("Enter server name = "))
    host['ip'] = str(input("Enter Host ip = "))
    host['port'] = int(input("Enter port number = "))
    host['coverage'] = float(input("Enter area coverage for the server in sq. m. (Default : 1 sq. m.) = "))
    if host['coverage'] < 1.0 :
        host['coverage'] = 1.0
    host['type'] = "local"

    quality = int(input("Enter input quality parameter (allowed : 1 to 60, default : 15) = "))
    if quality < 1 or quality > 60:
        host['quality'] = 480
    else:
        host['quality'] = quality*32

    serverFile = open("cc-6/server.json","w")
    json.dump(host, serverFile)
else:
    serverFile = open("cc-6/server.json","r")
    host = json.load(serverFile)

serverFile.close()

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

time.sleep(4.0)


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


def init_service():
    os.chdir(os.getcwd()+'/cc-6')
    os.system('virtualenv --system-site-packages venv_gpu_local')
    os.system('venv_gpu_local\\Scripts\\pip3 install -r requirements.txt')
    print("\n\n********** Initializing *********")
    os.system('venv_gpu_local\\Scripts\\python app.py')


if __name__ == "__main__":
    threading.Timer(2.0,force_start).start()
    app.run(host=host['ip'], port=host['port'], debug=False, threaded=True, use_reloader=False)
