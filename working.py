import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import cv2
import pytesseract
import picamera

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640, 480))

time.sleep(0.1)

	# grab the raw NumPy array representing the image, then initialize the timestamp
	# and occupied/unoccupied text
	# show the frame
	
face_cascade = cv2.CascadeClassifier('cascade.xml')

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

#         #print(left,top,right,bottom)
#         #print(max_bottom,max_right)

    if top < min_top:
        top = min_top
    if left < min_left:
        left = min_left
    if bottom > max_bottom:
        bottom = max_bottom
    if right > max_right:
        right = max_right
    return [left,top,right-left,bottom-top]   

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.08, 2, minSize=(36, 10),maxSize=(36*40, 10*40))
    # faces = face_cascade.detectMultiScale(gray,1.08, 5, minSize=(56, 20),maxSize=(56*40, 20*40))

    for (x,y,w,h) in faces:
        x -= w * 0.10
        w += w * 0.30
        y -= h * 0.15
        h += h * 0.3


        cv2.rectangle(img,(int(x), int(y)), (int(x + w), int(y + h)), (0, 255, 0), 1)
        cropped = cropImage(img, (int(x), int(y), int(w), int(h)))
        print(pytesseract.image_to_string(cropped))
        cv2.imwrite("cropped.jpg", cropped) 
    cv2.imshow("Frame", img)
    key = cv2.waitKey(1) & 0xFF
    # clear the stream in preparation for the next frame
    rawCapture.truncate(0)
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# cap.release()
# cv2.destroyAllWindows()