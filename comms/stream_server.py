import threading

from flask import Flask, Response, request
from comms.global_frame import get_current_frame, set_current_frame
import time

app = Flask(__name__)

def generate_stream(cam_id):
    while True:
        frame = get_current_frame(cam_id)
        if frame:
            break
        time.sleep(0.05)
    while True:
        frame = get_current_frame(cam_id)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        time.sleep(0.03)

@app.route('/video_feed')
def video_feed():
    cam_id = request.args.get('cam', 'default_cam')
    return Response(generate_stream(cam_id), mimetype='multipart/x-mixed-replace; boundary=frame')


import socket

def is_port_in_use(host, port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex((host, port)) == 0

def start_flask():
    if is_port_in_use('0.0.0.0', 5000):
        print("Flask already running")
        return

    print("Starting Flask server")
    app.run(host='0.0.0.0', port=5000, threaded=True)