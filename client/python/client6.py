#!/usr/bin/env python

import random
import socket, select
import time
from random import randint
import cv2
import numpy as np

vid = "C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\client\\python\\test1.mp4"
FREQ = 1
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (SERVER, PORT)

client.connect(server_address)
print("connecetd")


while True:
    buffSize = client.recv(HEADER)
    print("received header")
    if(buffSize):
        buffSizeStr = buffSize.decode(FORMAT)
        buffSizeInt = int(buffSizeStr)
        print(f'Data size: {buffSizeStr}')
        client.send(("OK").encode(FORMAT))
        print("sent ok")
        buff = client.recv(buffSizeInt)
        print("received data")
        dt = np.dtype(np.uint8)
        dt = dt.newbyteorder('>')
        frameNpArr = np.frombuffer(buff, dtype=dt) 
        f = open('data.png', 'wb')
        f.write(frameNpArr)
        f.close()
        frameDec = cv2.imdecode(frameNpArr, cv2.IMREAD_COLOR)
        frame = cv2.resize(frameDec, (400, 400), interpolation = cv2.INTER_AREA)
        print("decoded data")
        client.send(("DN").encode(FORMAT))
        print("sent dn")
        #cv2.imshow("Frame ", cv2.imread('C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\data.png'))
        cv2.imshow("ssdf", frame)
        cv2.waitKey(1)

