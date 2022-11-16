from asyncio.windows_events import CONNECT_PIPE_MAX_DELAY
import socket
import threading
import cv2
import base64
import imutils
import numpy as np

HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f'[NEW CONNECTION] {addr} connected.')

    connected = True
    while connected:
        msg_len = conn.recv(HEADER).decode(FORMAT)
        if(msg_len):
            msg_len = int(msg_len)
            msg = conn.recv(msg_len).decode(FORMAT)
            if(msg == DISCONNECT_MSG):
                connected = False

            print(f'{addr} : {msg}')
            npdata = np.fromstring(msg,dtype=np.uint8)
            frame = cv2.imdecode(npdata,1)
            f = open('bb.jpg', 'w')
            print(msg, file=f)
            f.close()
            #cv2.imshow("RECEIVING VIDEO",frame)


def start():
    server.listen()
    while True:
        l = input()
        if l == "q": 
            exit()
        conn, addr = server.accept()
        thread = threading.Thread(target = handle_client, args = (conn, addr))
        thread.start()
        #handle_client(conn, addr)
        print(f'[ACTIVE CONNECTION] {threading.active_count() -1}')
        
        

print("server is startung")
start()    


