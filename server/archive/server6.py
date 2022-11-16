from asyncio.windows_events import CONNECT_PIPE_MAX_DELAY
import socket
import threading
import cv2
import base64
import imutils
import numpy as np
import time 
from PIL import Image

FREQ = 1
HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
print(SERVER)
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
      
        try:
        
            vid = cv2.VideoCapture('C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\test1.mp4')
            print("vid")
            time.sleep(1/FREQ)
            while vid.isOpened():
                ret,frame = vid.read()
                frame = cv2.resize(frame, (400, 400), interpolation = cv2.INTER_AREA)
                print('read')
                frameEnc = cv2.imencode('.png', frame)[1] 
                frameNpArr = np.array(frameEnc)
                print(f'TYPE: { type(frameNpArr[0]) }')
                frameBytes = frameNpArr.tobytes()
                f = open('data.data', 'wb')
                f.write(frameNpArr)
                f.close()
                frameSize = len(frameBytes)
                frameSizeEnc = str(frameSize).encode(FORMAT)
                conn.send(frameSizeEnc)
                print("sent")

                response = conn.recv(HEADER)
                responseDec = response.decode(FORMAT)
                print(str(responseDec))
                while(str(responseDec) != "OK"):
                    pass

                
                conn.send(frameBytes)
                print("sent frame")
                response = conn.recv(HEADER)
                responseDec = response.decode(FORMAT)
                print("received data")
                while(str(responseDec) != "DN"):
                    pass
                
                time.sleep(1/FREQ)

        finally:
            print("client closed")
            conn.close()




        


def start():
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        #handle_client(conn, addr)
        print(f'[ACTIVE CONNECTION] {threading.active_count() -1}')
        
        

print("server is starting")
start()    

print("server closed")

