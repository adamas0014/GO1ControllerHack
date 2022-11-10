from flask import Flask, render_template, Response, request
import cv2
import time
from flask_cors import CORS
import json
import threading
import queue
import serial


processVideoIn = queue.Queue()
processVideoOut = queue.Queue()
processVideoEnd = threading.Event()

hardwareControlIn = queue.Queue()
hardwareControlOut = queue.Queue()
hardwareControlEnd = threading.Event()

controlLoopIn = queue.Queue()
controlLoopOut = queue.Queue()
controlLoopEnd = threading.Event()



def processVideo(inQueue, outQueue, returnThread):
    print("processVideo has started")
    while returnThread:
        frame = inQueue.get()
        time.sleep(0.02)    #just simulating the frame being processed
        outQueue.put(frame)
        #cv2.imshow("sfsd", frame)
        #cv2.waitKey(0)
    
    print("Leaving processVideo")
    cv2.destroyAllWindows()


def hardwareControl(inQueue, outQueue, returnThread):
    print("Inside hardwarecontrol")
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.port = 'COM4'
    ser.open()
    
    while( not ser.is_open):
        print("Trying to open Serial")
        time.sleep(1000)
        ser.open()
    print("Serial opened")    

    print("hardwareControl has started")
    while returnThread:
        ins = inQueue.get()
        print(ins)
        if( "cmd" in ins.keys()):

            if (ins["cmd"] == 'S'):
                print("Stop")
                ser.write('S\n'.encode('UTF-8'))
                outQueue.put("Stop OK")

            elif(ins["cmd"] == 'F'):
                print("Fwd")
                ser.write('F\n'.encode('UTF-8'))
                outQueue.put("Fwd OK")

            elif (ins["cmd"] == 'B'):
                print("Bwd")
                ser.write('B\n'.encode('UTF-8'))
                outQueue.put("Bwd OK")

            elif (ins["cmd"] == 'L'):
                print("left")
                ser.write('L\n'.encode('UTF-8'))
                outQueue.put("Left OK")

            elif (ins["cmd"] == 'R'):
                print("Right")
                ser.write('R\n'.encode('UTF-8'))
                outQueue.put("Right OK")

        if( "speed" in ins.keys()):
            print(f'Speed change: {ins["speed"]}')
            outQueue.put(f'{ins["speed"]} OK')

        if( "mode" in ins.keys()):
            print(f'Changing mode to: {ins["mode"]}')
            outQueue.put(f'{ins["mode"]} OK')

    ser.close()
    print("Leaving hardwareControl()")


def controlLoop(inQueue, outQueue, returnThread, config):

    while returnThread:
        setpoint = inQueue.get()


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
            vProcess = threading.Thread(target=processVideo, args=(processVideoIn, processVideoOut, processVideoEnd))
            cProcess = threading.Thread(target=hardwareControl, args=(hardwareControlIn, hardwareControlOut, hardwareControlEnd))
            vProcess.start()
            cProcess.start()
            app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)

        elif(choice == "stop"):
            print("Stopping threads...")
            processVideoEnd.set()
            hardwareControlEnd.set()
            print("Threads stopped")
            exitCall = True
    

app = Flask(__name__)
CORS(app)




class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture("C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\test1.mp4")    #"C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\test1.mp4"
        self.coverFrame = cv2.imread("C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\done.jpg")

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

def gen(camera):
    while True:
        frame = camera.get_frame()
        processVideoIn.put(frame)
        frame = processVideoOut.get()

        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
  
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/controls', methods = ["POST"], strict_slashes = False)
def control():
    if(request.method == "POST"):
        data = json.loads(request.data.decode('utf-8'))
        hardwareControlIn.put(data)
        print(data)
        resp = hardwareControlOut.get()
        return Response(resp)



if __name__ == '__main__':
    menuThread = threading.Thread(target=menu, args=tuple())
    menuThread.start()
    exit(0)