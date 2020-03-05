import os
import cv2
from base_camera import BaseCamera
import pytesseract
import json
import paho.mqtt.client as mqtt #import the client1
broker_address="mqtt.eclipse.org"
port = 80 
# #broker_address="iot.eclipse.org" #use external broker
list = { 
        "GJ21AQ8052":{
            "number" : "GJ21AQ8052",
            "name": "vasu",
            "car_model" : "i20",
            "mob": 9033195859
            },
        "MH01BG2654":{
            "number" : "MH01BG2654",
            "name": "Manish",
            "car_model" : "BMW",
            "mob": 9904496237
            }
                
        }
face_cascade = cv2.CascadeClassifier('cascade.xml')
client = mqtt.Client("client-socks",transport='websockets')
client.connect(broker_address,port) #connect to broker
# img = cv2.imdecode(buff, 1)
# # cap = cv2.VideoCapture(0)


def cropImage(image,rect):
    x, y, w, h = computeSafeRegion(image.shape,rect)
    return image[y:y+h,x:x+w]

def computeSafeRegion(shape,bounding_rect):
    top = bounding_rect[1] # y
    bottom  = bounding_rect[1] + bounding_rect[3] # y +  h
    left = bounding_rect[0] # x
    right =   bounding_rect[0] + bounding_rect[2] # x +  w
    min_top = 0
    max_bottom = shape[0]
    min_left = 0
    max_right = shape[1]
    if top < min_top:
        top = min_top
    if left < min_left:
        left = min_left
    if bottom > max_bottom:
        bottom = max_bottom
    if right > max_right:
        right = max_right
    return [left,top,right-left,bottom-top]   

class Camera(BaseCamera):
    video_source = 0
    status = False
    def __init__(self):
        self.data = 1
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()
        

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        
        for frame1 in BaseCamera.camera.capture_continuous(BaseCamera.rawCapture, format="bgr", use_video_port=True):
            img = frame1.array
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)            
            # faces = face_cascade.detectMultiScale(gray,1.08, 2, minSize=(36, 10),maxSize=(36*40, 10*40))
            faces = face_cascade.detectMultiScale(gray,1.08, 5, minSize=(56, 20),maxSize=(56*40, 20*40))
            font = cv2.FONT_HERSHEY_SIMPLEX
            client.loop_start()
            for (x,y,w,h) in faces:
                x -= w * 0.10
                w += w * 0.30
                y -= h * 0.15
                h += h * 0.3
                cv2.rectangle(img,(int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 1)
                cropped = cropImage(img, (int(x), int(y), int(w), int(h)))
                rec = pytesseract.image_to_string(cropped)
                if '$' in rec:
                    rec = rec.replace('$','s')
                if rec:
                    s = len(rec)
                    for i in list.keys():
                        if rec[s-4:] in i:  
                            client.publish('/data', json.dumps(list[i]))
                    
                cv2.putText(img,rec,(2,170),font,1,(0,255,0),2,cv2.LINE_AA)
                # print(pytesseract.image_to_string(cropped))
                cv2.imwrite("cropped.jpg", cropped) 
            # client.publish("/data","OFF")#publish
                    
            yield cv2.imencode('.jpg', img)[1].tobytes()
            BaseCamera.rawCapture.truncate(0)
            if Camera.status:
                break
