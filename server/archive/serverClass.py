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

parser = argparse.ArgumentParser(description="Start the GO1 Hack Studio server")
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--config', type=str, default="_config.json", required=False, help="Use a non-default configuration script")
group.add_argument('-a', '--autostart', type=bool, required=True, help="Decide whether to load server in CLI mode")
group.add_argument('-v', '--verbose', type=bool, default=False, required=False, help="Print additional server state info")
args = parser.parse_args()

class Server():
    def __init__(self, flaskApp, mqttClient, videoSource):
        self._configParser = ConfigParser(args.config)
        self._app = flaskApp
        self._mqttClient = mqttClient
        self._videoSource = videoSource
        self._processVideo = None
        self._t = dict()
    
    def createEventThread(self, name: str, fn: function, eventList: list):
        if(self._t[name] != None):
            print("!Error, thread already exists")
            return False

        try:
            returnEvent = threading.Event()
            events = dict()

            if( len(eventList) > 0 ):
                for e in eventList:
                    events({str(e): threading.Event()})
        
            queueIn = queue.Queue()
            queueOut = queue.Queue()
            thread = threading.Thread(target=fn, args=(queueIn, queueOut, returnEvent, events))
            
            self._t[name] = dict({
                "return": returnEvent,
                "qIn": queueIn,
                "qOut": queueOut,
                "thread": thread,
                "events": events
            })
            
        except:
            return None

        return self._t[name]

    #Delete once createEventThread works
    def createThread(self, name: str, fn: function):
        if(self._t[name] != None):
            print("!Error, thread already exists")
            return False

        returnEvent = threading.Event()
        queueIn = queue.Queue()
        queueOut = queue.Queue()
        thread = threading.Thread(target=fn, args=(queueIn, queueOut, returnEvent))

        self._t[name] = dict({
                "return": returnEvent,
                "qIn": queueIn,
                "qOut": queueOut,
                "thread": thread
            })
            
        return True

    def startAllThreads(self):
        for key, val in self._t.items():
            val["thread"].start()
    
    def returnAllThreads(self):
        for key, val in self._t.items():
            val["return"].set()


    #
    #   THREADED PROCESSES
    #

    def flaskServer(self, queueIn, queueOut, returnEvent, events):
        if(not returnEvent):
            return
        
    def videoProcessing(self, queueIn, queueOut, returnEvent, events):
        while not returnEvent:
            pass

        return

    def hardwareControl(self, queueIn, queueOut, returnEvent, events):
        mqttClient = mqtt.Client()
        mqttClient.on_message = self.on_message
        mqttClient.on_connect = self.on_connect
        mqttClient.on_publish = self.on_publish
        mqttClient.on_subscribe = self.on_subscribe
        mqttClient.on_log = self.on_log


        ser = serial.Serial()
        ser.baudrate = 9600
        ser.port = 'COM7'
        ser.open()
        
        
        speedCnf = "Medium"
        mode = "Manual"

        while not returnEvent:
            while mode == "Manual" :
                while not ser.is_open:
                    if args.verbose: print("Trying to open Serial")
                    time.sleep(2)
                    ser.open()

                    if args.verbose: print("Serial opened")

                ins = queueIn.get()
                insL = ins.split(' ')

                if(insL[0] == 'CMD'):
                    mcuSend = str()
                    response = str()

                    if(insL[1] == 'S'):
                        ser.write(('0.00 0.00 0.00 0.00\n').encode('UTF-8'))
                        response = "Stop OK"

                    elif(insL[1] == 'F'):
                        ser.write((f'0.00 0.00 {round(self._config[speedCnf]["ly"], 2)} 0.00\n').encode('UTF-8'))
                        response = "Forward OK"

                    elif(insL[1] == 'B'):
                        ser.write((f'0.00 0.00 { - round(self._config[speedCnf]["ly"], 2)} 0.00\n').encode('UTF-8'))
                        response = "Backward OK"

                    elif(insL[1] == 'L'):
                        ser.write((f'0.00 {round(self._config[speedCnf]["rx"], 2)} 0.00 0.00\n').encode('UTF-8'))
                        response = "Left OK"

                    elif(insL[1] == 'R'):
                        ser.write((f'0.00 { - round(self._config[speedCnf]["rx"], 2)} 0.00 0.00\n').encode('UTF-8'))
                        response = "Right OK"

                    else:
                        ser.write(('0.00 0.00 0.00 0.00\n').encode('UTF-8'))
                        response = "Stop OK"

                elif(insL[0] == 'CNF'):
                    if(insL[1] == 'S'):
                        speedCnf = insL[2]
                        response = '{speedCnf} OK'

                    elif (insL[1] == 'A'):
                        speedCnf = "Slow"
                        mode = "Automatic"
                        response = "Automatic OK"

                    else:
                        response = "Unknown Configuration Command"                    
            
            while mode == "Automatic" :
                horizontalOffset = 


        return
    
    def __str__(self):
        t = time.time()
        tState = dict({})

        for key, val in self._t.items():
            tState[key] = val["thread"].getState()


        return dict({
            "time": t,
            "Thread States": tState           
        })

    def initialize(self):
        try:
            self.loadConfig()
        except:
            if(args.verbose) : print("! - Failed to load configuration file")

        try:
            if(args.autostart):
                #if its autostart, we want to thread the flask server
                self._app.debug = False
                self._use_reloader = False   
                self.createEventThread("Flask", self.flaskServer, [None])
            
            else:
                self.flaskServer(None, None, None, None) #lol none none none 
        except:
            if args.verbose: print("! - An error occurred when initializing the flask server")
        
        try:
            self.createEventThread("VideoProcessing", self.videoProcessing, ["Preprocess"])
        except:
            if args.verbose: print("! - An error occurred when initializing the preprocess thread")
        
        try:
            self.createEventThread("HardwareControl", self.hardwareControl, ["Ramp"])
        except:
            if args.verbose: print("! - An error occurred when initializing the hardware control thread")
      

    def start(self):
        self._timestamp = time.time()
        try:
            self.startAllThreads()
        except:
            if(args.verbose): print("! - Some threads failed to start")


    def loadConfig(self):
        self._config = self._configParser.load()
        print(str(self._config))
        return self._config

    def menu(self):
       
        print(" \n \
            start - start server    \n \
            stop - stop server      \n \
            \n \
            ")
        choice = input()
        if(choice == "start"):
            self.createThread("ProcessVideo", )
            self.createThread("CommandParser", )
            self.startAllThreads()
            self._app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)
        elif(choice == "stop"):
            print("Stopping threads...")
            self.returnAllThreads()
            print("Threads stopped")
                
    
    def spin(self):
        if(args.verbose):
            elapsed = self._timestamp - time.time()
            self._timestamp = time.time()

            if(elapsed > 60):
                print(str(self))

        if(not args.autostart):
            while(True):
                self.menu()
            
        else:
            return
            
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


def main():


    app = Flask(__name__)
    CORS(app)

    server = Server(app, -1)
    server.initialize()
    server.start()

    while(True):
        server.spin()
        

    return









if __name__ == "__main__":
    main()