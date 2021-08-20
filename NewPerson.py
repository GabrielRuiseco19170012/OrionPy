from datetime import datetime
import cuid
from MongoDB import MongoDB
from ApiRequest import ApiConsumption
from picamera import Picamera
from time import sleep

newMongo = MongoDB()
newMongo.mongoConnect()
class Person(object):

    def __init__(self):
        self.photo = None
        self.face_token = None

    def sendData(self):
        try:
            camera = Picamera()
            camera.start_preview(alpha=192)
            sleep(1)
            camera.capture("/home/pi/Desktop/Orion/pic.jpg")
            camera.stop_preview()
            id = ApiConsumption.user.getID()
            resp = ApiConsumption.uploadFile("/home/pi/Desktop/Orion/pic.jpg")
            now = datetime.now()
            self.photo = resp.get('photo')
            self.face_token = resp.get('face_token')
            data = {'photo': self.photo, 'idUser': id, "face_token": self.face_token, "created_at": now}
            newMongo.insertData(data)
        except Exception as err:
            print(err)