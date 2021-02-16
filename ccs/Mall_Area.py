import pyrebase
import json

pyrebaseFile = open("cc-6/pyrebase.json","r")
firebaseConfig = json.load(pyrebaseFile)
pyrebaseFile.close()

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()


def mall_area(area):
    global db
    db.child("Mall").child("area").set(str(area))

area = input("Enter total mall area in sq. m. = ")
mall_area(area)
