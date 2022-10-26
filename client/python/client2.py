import socket
import cv2
import imutils
import base64
vid = cv2.VideoCapture('./test1.mp4') 


HEADER = 64
PORT = 5050
SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MSG = "!DISCONNECT"
SERVER  = socket.gethostbyname(socket.gethostname())

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_len = len(message)
    send_len = str(msg_len).encode(FORMAT)
    send_len += b' ' * (HEADER - len(send_len))
    client.send(send_len)
    client.send(message)


def send64(msg):
    encoded, buffer = cv2.imencode('.jpg',msg,[cv2.IMWRITE_JPEG_QUALITY,80])
    msg_len = str(len(buffer)).encode(FORMAT)
    message = str(buffer).encode(FORMAT)
    client.send(msg_len)
    client.send(message)

vid = cv2.VideoCapture('./test1.mp4') 

while(vid.isOpened()):
    _,frame = vid.read()
    print('c')
    frame = imutils.resize(frame,width=400)
    send64(frame)







