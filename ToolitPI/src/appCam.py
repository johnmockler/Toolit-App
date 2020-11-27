from flask import Flask, render_template, Response
# Raspberry Pi camera module (requires picamera package, developed by Miguel Grinberg)
from camera_pi import Camera
from inc import imagezmq
from PIL import Image
import time
import socket


app = Flask(__name__)
cap = 0

SERVERNAME = '192.168.2.102'

sender = imagezmq.ImageSender(connect_to="tcp://" + SERVERNAME + ":5555")

rpiName = socket.gethostname()

send_status = ''


@app.route('/')
def index():
    global send_status
    """Video streaming home page."""
    return render_template('index.html', status = send_status)

def gen(camera):
    """Video streaming generator function."""
    global cap
    global send_status
    while True:        
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        if (cap==1):
                try:
                    sender.send_jpg(rpiName,frame)
                    cap = 0
                    send_status = 'Image Transfer Successful'
                except:
                    cap = 0
                    send_status = 'There was a problem with the image transfer. Please Try Again...'

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/capture')
def capture():
    global cap
    global send_status
    cap = 1
    return render_template('index.html', status = send_status)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port =80, debug=True, threaded=True)

