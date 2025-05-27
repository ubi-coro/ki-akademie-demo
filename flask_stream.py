from flask import Flask, Response
import cv2
import numpy as np
import time

app = Flask(__name__)

def generate_frames():
    while True:
        frame = np.zeros((480, 640, 3), dtype=np.uint8)
        timestamp = time.strftime('%H:%M:%S.') + f'{int((time.time() % 1) * 1000):03d}'
        cv2.putText(frame, timestamp, (50, 240), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 3)
        _, jpeg = cv2.imencode('.jpg', frame)
        yield (b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n')
        time.sleep(0.01)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, threaded=True)