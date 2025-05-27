from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap

class ImageViewer(QLabel):
    def __init__(self):
        super().__init__()
        self.setScaledContents(True)

    def update_image(self, pixmap: QPixmap):
        self.setPixmap(pixmap)