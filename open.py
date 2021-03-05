import RPi.GPIO as GPIO
import time
import os
import pyrealsense2.pyrealsense2 as rs
import numpy as np
import cv2

import RPi.GPIO as GPIO
import time

import face_recognition
import numpy as np

import board
import neopixel

#######################
# Setting Up Motor
#######################
GPIO.setwarnings(False)

servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

######################
# Setting Up Camera
#####################
pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)


pipeline.start(config)

#####################
# Setting Up LED
#####################
pixels = neopixel.NeoPixel(board.D18, 5)

pixels.fill((255, 0, 0))

#####################
# Defining functions
#####################

def open_door():
    p = GPIO.PWM(servoPIN, 50) 
    pixels.fill((0, 255, 0))
    p.start(7.5) 
    time.sleep(0.5)
    p.ChangeDutyCycle(4.5)
    time.sleep(1)
    p.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    pixels.fill((255, 0, 0))

def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

###############################
# Setting up Faceial Recog
##############################

path = 'Images'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

encodeListKnown = findEncodings(images)
print('Encoding Complete')

try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        color_image = np.asanyarray(color_frame.get_data())
        #color_image = cv2.resize(color_image,(0,0),None,0.25,0.25)
        

        facesCurFrame = face_recognition.face_locations(color_image)
        encodesCurFrame = face_recognition.face_encodings(color_image,facesCurFrame)
        
        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace,tolerance = 0.4)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
    
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                if name == 'liangyu':
                    pass
                else:
                    open_door()
                print(name)
                y1,x2,y2,x1 = faceLoc
                #y1, x2, y2, x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(color_image,(x1,y1),(x2,y2),(0,0,255),2)
                cv2.rectangle(color_image,(x1,y2-35),(x2,y2),(0,0,255),cv2.FILLED)
                cv2.putText(color_image,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
    
        cv2.imshow('Webcam',color_image)
        if cv2.waitKey(1) == ord("q"):
                break
        
finally:
    #open_door()
    pipeline.stop()
    cv2.destroyAllWindows()
