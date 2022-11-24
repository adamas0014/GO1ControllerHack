import sys
import argparse
from flask import Flask, render_template, Response, request
import cv2
import time
from flask_cors import CORS
import json
import threading
import queue
import serial
from ConfigParser import ConfigParser
import paho.mqtt.client as mqtt
import numpy as np
import imutils
from pyzbar.pyzbar import decode

parser = argparse.ArgumentParser(description="Start the GO1 Hack Studio server")
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--config', type=str, default="_config.json", required=False, help="Use a non-default configuration script")
group.add_argument('-a', '--autostart', type=bool, required=False, help="Decide whether to load server in CLI mode")
group.add_argument('-v', '--verbose', type=bool, default=False, required=False, help="Print additional server state info")
args = parser.parse_args()

#Defining a function to calculate width of the QR Code (with the known distance) in pixels
def find_Pixel_Width_Image(image):
    for QR_Code in decode(image):   #Takes the image and decodes it as a QR Code, which returns different values such as the bounding box coordinates
        pixelWidthImage = QR_Code.rect[2]   #.rect is used because the width in pixels of the bounding box is stored in the second index of the list
    return pixelWidthImage

#Defining a function to calculate width of the QR Code in real time, identical to the function defined above
def find_Pixel_Width_Video(frame):
    for QR_Code in decode(frame):
        pixelWidthVideo = QR_Code.rect[2]
    return pixelWidthVideo

#Defining a function to calculate distance in inches using three parameters, known width, focalLength, and pixel width
def distance(knownWidth, focalLength, pixelWidth):
    return (knownWidth * focalLength) / pixelWidth

#Establishing known parameters for the intialization QR_Code image that is 50 inches away from the camera
KNOWN_DISTANCE = 65.0
KNOWN_WIDTH = 8.0

frameOut = queue.Queue()
posOut = queue.Queue()

def videoProcess():
    image = cv2.imread("C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\calibrationImage65in.jpg")
    KNOWN_PIXEL_WIDTH = find_Pixel_Width_Image(image)
    focalLength = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH #-> With the numbers, it is focalLength = 149 p * 65 in / 8 in = 931.25 p

    #Reading in live video capture
    cap = cv2.VideoCapture(0)

    while True:
        outData = list()
        ret = False
        while ret == False:
            ret, frame = cap.read()
            print("can't read frame")
            time.sleep(2)

        #Height and width of the frame in pixels is calculated 
        h, w = frame.shape[:2]
    
        #Circle is drawn at the center point of the frame
        cv2.circle(frame, (w//2, h//2), 3, (0, 255, 0), -1)
    
        #This represents every angle per perceived pixel in the frame, calculated by divindg horizontal FOV by the horizontal resolution of camera
        Angle_Factor = 48.8 / 1280
    
        for QR_Code in decode(frame):
            
            #The pixel width of the QR Code in live video is assigned to a variable by extracting the value from the function
            PIXEL_WIDTH = find_Pixel_Width_Video(frame)
            
            #All values are now computed, which allows for distance calculation
            inches = distance(KNOWN_WIDTH, focalLength, PIXEL_WIDTH)
            corrected = inches - 30
            inches_to_string = str(round(corrected, 2))
            
    
            #Polygon points (bottom left and top right) are extracted from the decode function 
            x1 = QR_Code.polygon[0][0]
            x2 = QR_Code.polygon[2][0]
            y1 = QR_Code.polygon[0][1]
            y2 = QR_Code.polygon[2][1]
            
            #Center point of the QR Code is calculated by finding the average of x and y
            x_center = (x1 + x2)//2
            y_center = (y1 + y2)//2
            
            #Bounding box is drawn around the QR Code using the polygon points of the QR Code
            pts = np.array([QR_Code.polygon], np.int32)
            pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0))
    
            #Circle is drawn at the center point of the QR Code
            cv2.circle(frame, (x_center, y_center), 3, (0, 0, 255), -1 )
    
            #Offset from the center point of the frame is calculated
            offset = x_center - w//2
            
            #An angle can be calcualted by multiplying offset by the angle per pixel value
            angle = offset * Angle_Factor
            outData = [offset, angle]
            #Text is added on top of the frame for better visualization
            cv2.putText(frame, inches_to_string + ' in', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, 2)
    
            #If statement is written to determine if QR Code is to the right or left depending if the offset is positive or negative
            if offset > 20:
                cv2.putText(frame, "QR is to the right from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' R ' + str(abs(angle)))
                #ser.write('R\n'.encode("UTF-8"))
                
                
            elif offset < -20:
                cv2.putText(frame, "QR is to the left from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' L ' + str(abs(angle)))
                #ser.write('L\n'.encode("UTF-8"))
                
            elif -20 < offset < 20:
                cv2.putText(frame, "QR is to the front from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' F ' + str(abs(angle)))
                #ser.write('F\n'.encode("UTF-8"))
        
        
        frameResize = cv2.resize(frame, (640, 480))
        cv2.imshow("frame", frameResize)

        frameOut.put(frameResize)
        posOut.put(outData)


        if cv2.waitKey(1) == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()   


def controlProcess():
    
    def on_connect(mqttc, obj, flags, rc):
        print("rc: " + str(rc))

    def on_message(mqttc, obj, msg):
        print(msg.topic + " " + str(msg.qos) + " " + str(msg.payload))

    def on_publish(mqttc, obj, mid):
        print("mid: " + str(mid))
        pass

    def on_subscribe(mqttc, obj, mid, granted_qos):
        print("Subscribed: " + str(mid) + " " + str(granted_qos))

    def on_log(mqttc, obj, level, string):
        print(string)

    mqttc = mqtt.Client()
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    mqttc.on_log = on_log

    mqttc.connect("192.168.12.1", 1883, 60)

    mqttc.loop_start()

    infot = mqttc.publish("controller/action", "standDown", qos=2)
    infot.wait_for_publish()
    time.sleep(2)
    infot = mqttc.publish("controller/action", "standUp", qos=2)
    infot.wait_for_publish()
    time.sleep(2)
    infot = mqttc.publish("controller/action", "recoverStand", qos=2)
    infot.wait_for_publish()
    time.sleep(2)
    infot = mqttc.publish("controller/action", "walk", qos=2)
    infot.wait_for_publish()
    time.sleep(2)

    while True:
        x = posOut.get()

def main():
    videoProcess()
    #controlProcess()








if __name__ == "__main__":
    main()