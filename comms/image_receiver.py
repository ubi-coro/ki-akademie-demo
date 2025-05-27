import zmq
import threading
import numpy as np
import cv2
from PyQt6.QtGui import QImage, QPixmap

def recv_image():
    context = zmq.Context()
    socket = context.socket(zmq.SUB)
    socket.connect("tcp://localhost:5555")
    socket.setsockopt_string(zmq.SUBSCRIBE, '')
    return socket

def start_image_thread(callback):
    def run():
        socket = recv_image()
        while True:
            img_bytes = socket.recv()
            np_img = np.frombuffer(img_bytes, dtype=np.uint8)
            img = cv2.imdecode(np_img, cv2.IMREAD_COLOR)
            h, w, ch = img.shape
            qimg = QImage(img.data, w, h, ch * w, QImage.Format.Format_BGR888)
            pixmap = QPixmap.fromImage(qimg)
            callback(pixmap)
    threading.Thread(target=run, daemon=True).start()