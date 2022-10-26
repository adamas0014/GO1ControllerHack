import socket

from pathlib import Path
import cv2
import os


print(os.path.dirname(os.path.abspath(__file__)))

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 1002))

vid = cv2.VideoCapture('C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\client\\python\\test1.mp4')

while vid.isOpened():
    _,frame = vid.read()
    fEnc = str(frame).encode('utf-8')
    #print(fEnc)
    print(len(fEnc))
    data = str(len(fEnc)).encode('utf-8') + ' ' + fEnc
    client.send(data)

    

# #file = open('C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\client\\python\\tux1.png', 'rb')
# #image_data = file.read(2048)

# while image_data:
#     client.send(image_data)
#     image_data = file.read(2048)

#file.close()
client.close()