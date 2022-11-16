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


parser = argparse.ArgumentParser(description="Start the GO1 Hack Studio server")
group = parser.add_mutually_exclusive_group()
group.add_argument('-c', '--config', type=str, default="_config.json", required=False, help="Use a non-default configuration script")
group.add_argument('-a', '--autostart', type=bool, required=True, help="Decide whether to load server in CLI mode")
group.add_argument('-i', '--ipaddress', type=str, default=False, required=False, help="Use a non-default ip address for the quadruped")
group.add_argument('-v', '--verbose', type=bool, default=False, required=False, help="Print additional server state info")
args = parser.parse_args()

class Server():
    def __init__(self, flaskApp, mqttClient, commandParser, videoSource):
        self._configParser = ConfigParser(args.config)
        self._app = flaskApp
        self._mqttClient = mqttClient
        self._commandParser = commandParser
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

    def initialize(self):
        if(args.autostart):
            #if its autostart, we want to thread the flask server
            app.debug = False
            app.use_reloader=False

            def flaskServer(queueIn, queueOut, returnEvent, events):
                if(not returnEvent):
                    return
                
            self.createEventThread(lambda: while(returnThread):  )
    
    def start(self):
        pass

    def loadConfig(self):
        self._config = self._configParser.load()
        print(str(self._config))

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
        if(not args.autostart):
            while(True):
                self.menu()
            
        else:
            



def main():

    return









if __name__ == "__main__":
    main()