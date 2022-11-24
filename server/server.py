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
from PIL import Image

processVideoIn = queue.Queue()
processVideoOut = queue.Queue()
processVideoEnd = threading.Event()

hardwareControlIn = queue.Queue()
hardwareControlOut = queue.Queue()
hardwareControl = threading.Event()

automaticMode = threading.Event()
commandQueue = queue.Queue()

coverFrame = cv2.imread("C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\archive\\done.jpg")



def processVideo(outCommand, outFrame, returnThread):

    print("inside proceess video")
    #Defining a function to calculate width of the QR Code (with the known distance) in pixels
    def find_Pixel_Width_Image(image):
        for QR_Code in decode(image):   #Takes the image and decodes it as a QR Code, which returns different values such as the bounding box coordinates
            pixelWidthImage = QR_Code.rect[2]   #.rect is used because the width in pixels of the bounding box is stored in the second index of the list
        return pixelWidthImage
    print("2")
    #Defining a function to calculate width of the QR Code in real time, identical to the function defined above
    def find_Pixel_Width_Video(frame):
        for QR_Code in decode(frame):
            pixelWidthVideo = QR_Code.rect[2]
        return pixelWidthVideo
    print("3")
    #Defining a function to calculate distance in inches using three parameters, known width, focalLength, and pixel width
    def distance(knownWidth, focalLength, pixelWidth):
        return (knownWidth * focalLength) / pixelWidth

    #Establishing known parameters for the intialization QR_Code image that is 50 inches away from the camera
    KNOWN_DISTANCE = 65.0
    KNOWN_WIDTH = 8.0

    image = cv2.imread("C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\calibrationImage65in.jpg")
    KNOWN_PIXEL_WIDTH = find_Pixel_Width_Image(image)
    focalLength = (KNOWN_PIXEL_WIDTH * KNOWN_DISTANCE) / KNOWN_WIDTH #-> With the numbers, it is focalLength = 149 p * 65 in / 8 in = 931.25 p
    print("4")
    #Reading in live video capture
    cap = cv2.VideoCapture(0)

    while returnThread:
        #print ("loopy loop")
        
        ret = False
        while ret == False:
            ret, frame = cap.read()

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
        
            #Text is added on top of the frame for better visualization
            cv2.putText(frame, inches_to_string + ' in', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 1, 2)
    
            #If statement is written to determine if QR Code is to the right or left depending if the offset is positive or negative
            if offset > 20:
                cv2.putText(frame, "QR is to the right from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' R ' + str(abs(angle)))
                #ser.write('R\n'.encode("UTF-8"))
                outCommand.put(dict({"MODE": "A", "CMD": 'R'}))
               
                
            elif offset < -20:
                cv2.putText(frame, "QR is to the left from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' L ' + str(abs(angle)))
                #ser.write('L\n'.encode("UTF-8"))
                outCommand.put(dict({"MODE": "A", "CMD": 'L'}))
            
            elif -20 < offset < 20 and inches > 100:
                cv2.putText(frame, "QR is to the front from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' F ' + str(abs(angle)))
                #ser.write('F\n'.encode("UTF-8"))
                outCommand.put(dict({"MODE": "A", "CMD": 'F'}))
            
            elif -20 < offset < 20 and inches < 50:
                cv2.putText(frame, "QR is to the front from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' B ' + str(abs(angle)))
                #ser.write('F\n'.encode("UTF-8"))
                outCommand.put(dict({"MODE": "A", "CMD": 'B'}))

            else:
                cv2.putText(frame, "QR is to the front from the robot POV, " + str(abs(round(angle,2))) + " degrees from the camera centre", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, 2)
                print(inches_to_string + ' ELSE ' + str(abs(angle)))


        #print("Frame resize")
        frameResize = cv2.resize(frame, (640, 480))
        #cv2.imshow("frame", frameResize)
        #print("trying to push frame to queue")
        if outFrame.qsize() < 15:
            outFrame.put(frameResize)
            #print('frame pushed to queue')

        if cv2.waitKey(1) == ord('q'):
            break
        
    #cv2.destroyAllWindows()   

def controlLoop(inQueue, outQueue, returnThread, automaticMode):
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

    while returnThread:
        ins = dict({})
        
        modeFilter = 'M'

        if automaticMode.is_set():
           modeFilter = 'A' 
           print("automatic mode")
            

        while((not 'MODE' in ins) or ins['MODE'] != modeFilter):
            ins = inQueue.get()
            #print("inQueue not right mode")
        
        if ins["CMD"] == 'S':
            infot = mqttc.publish("controller/stick", b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00", qos=2)
            outQueue.put("S OK")
            print('s')

        elif ins["CMD"] == 'B':
            infot = mqttc.publish("controller/stick", b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\xf8\r\xbf", qos=2) #bwd
            outQueue.put("B OK")
            print('b')

        elif ins["CMD"] == 'F':
            infot = mqttc.publish("controller/stick", b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00$\xf8\r?", qos=2) #fwd
            outQueue.put("F OK")
            print('f')
            
        elif ins["CMD"] == 'L':
            infot = mqttc.publish("controller/stick", b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x00", qos=2)
            outQueue.put("L OK")
            print('l')

        elif ins["CMD"] == 'R':
            infot = mqttc.publish("controller/stick", b"\x00\x00\x00\x00\x00\x00\x80?\x00\x00\x00\x00\x00\x00\x00\x00", qos=2) # turn right
            outQueue.put("R OK")
            print('r')

        else:
            print("Unrecognized command")
            outQueue.put("FAILURE")
        
            


    





def menu():
    exitCall = False

    while not exitCall:
        print(" \n \
            start - start server    \n \
            stop - stop server      \n \
            \n \
        ")
        choice = input()
        if(choice == "start"):
            vProcess = threading.Thread(target=processVideo, args=(commandQueue, processVideoOut, processVideoEnd))
            cProcess = threading.Thread(target=controlLoop, args=(commandQueue, hardwareControlOut, processVideoEnd, automaticMode))
            vProcess.start()
            cProcess.start()
            automaticMode.clear()
             
            app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False, debug = True)
            print(str(app))
        elif(choice == "stop"):
            print("Stopping threads...")
            processVideoEnd.set()
            print("Threads stopped")
            exitCall = True
    

app = Flask(__name__)
CORS(app)




class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0) 
        self.coverFrame = cv2.imread("C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\archive\\done.jpg")

    def __del__(self):
        self.video.release() 
        return  

    def get_frame(self):
        ret, frame = self.video.read()

        if frame is None:
            frame = self.coverFrame
            print("out of frames")
            time.sleep(1)

        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()



@app.route('/')
def index():
    return render_template('index.js')

def gen():
    start = time.time()
    while True:
        if not processVideoOut.empty():
            frame = processVideoOut.get()
            print('got frame')
        else:
            end = time.time()
            if(end - start > 10):
                frame = coverFrame
                print('didnt retrieve frame')
                start = end

        ret, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
  


@app.route('/video_feed')
def video_feed():
    return Response(gen(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')



@app.route('/controls', methods = ["POST"], strict_slashes = False)
def control():
    if(request.method == "POST"):
        data = json.loads(request.data.decode('utf-8'))
        print("received command from client: ", str(data))
        if not "MODE" in data:
            print("No mode was set")

        elif(data["MODE"] == 'A'):
            automaticMode.set()

        elif (data["MODE"] == 'M'):
            automaticMode.reset()

        if(not automaticMode.is_set()):
            commandQueue.put(dict({"MODE": "M", "CMD": data['CMD']})) 
            val = dict({"MODE": "M", "CMD": data['CMD']})
            print(f'to mqtt: {val}')   
                  
        resp = str()
        while not hardwareControlOut.empty():
            resp += hardwareControlOut.get() + "\n"

        return Response(resp)



if __name__ == '__main__':
    menuThread = threading.Thread(target=menu, args=tuple())
    menuThread.start()
    exit(0)