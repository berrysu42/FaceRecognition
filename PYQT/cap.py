import sys

import cv2

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from PyQt5.QtCore import QTimer
from PyQt5.QtCore import Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PYQT APP")
        self.setFixedSize(640,360)



        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

        self.frame_label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.frame_label)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.updateFrame)
        self.timer.start(30)
        self.show()
    def updateFrame(self):
        ret,frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            frame = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)


            pixmap_frame =QPixmap.fromImage(frame)
            self.frame_label.setPixmap(pixmap_frame.scaled(self.frame_label.size(),Qt.KeepAspectRatio,Qt.SmoothTransformation))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())