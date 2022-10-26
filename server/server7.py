from flask import Flask, render_template, Response, request
import cv2
import time
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)


class VideoCamera(object):
    def __init__(self):
      self.video = cv2.VideoCapture(0)    #"C:\\Users\\adama\\OneDrive\\Documents\\GitHub\\GO1ControllerHack\\server\\test1.mp4"
    def __del__(self):
        self.video.release() 
        return  

    def get_frame(self):
        ret, frame = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()



@app.route('/')
def index():
    return render_template('index.js')

def gen(camera):
    while True:
        frame = camera.get_frame()
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
        print(f'X: {data["x"]}, Y: {data["y"]}')
        return Response()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True, use_reloader=False)