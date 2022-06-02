import os
import cv2
import controllers.processImage as procI
from pynput.keyboard import Key, Listener
from PyQt5.QtCore import pyqtSignal, QThread, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtGui
import numpy as np

# Set up as a trhead so it can be run 
# along with PyQt window
class Camera(QThread):
    pixmap_signal = pyqtSignal(np.ndarray)

    # this camera definiton if for translation
    # to PyQt object
    # acual detail is set in run()
    def __init__(self):
        super().__init__()
        self.running = True
        self.cam_width = 640
        self.cam_height = 480

    # This runs after start() is called on the thread
    # set the camera detail here.
    # the better detailed camera the better image taken
    # problems with low resultion cameras arise because
    # image is cropped 
    def run(self):
        self.cam = cv2.VideoCapture(1)
        self.cam.set(cv2.CAP_PROP_FPS, 30.0)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
        # self.camWidth = self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)
        # self.camHeight = self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT)

        while(self.running):
            ret, frame = self.cam.read()
            #print((frame))
            if ret:
                self.pixmap_signal.emit(frame)
        self.cam.release()

    def stopCam(self):
        self.running = False
        self.wait()

    # converts the frame from a OpenCV image
    # to a PyQt Pixmap so it can be shown
    def convertFrame(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, ch = rgb_frame.shape
        line = ch * width
        qt_frame = QImage(rgb_frame.data, width, height, line, QImage.Format.Format_RGB888)
        scaled_frame = qt_frame.scaled(self.cam_width, self.cam_height, Qt.AspectRatioMode.KeepAspectRatio)
        return QPixmap.fromImage(scaled_frame)
