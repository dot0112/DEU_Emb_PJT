import cameraStreamThread
import WIFIIconThread
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt


class TranslateWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi("translate.ui", self)

        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")  # 완전 투명

        self.cameraStreamThread = cameraStreamThread.CameraStreamThread()
        self.cameraStreamThread.update_frame.connect(self.update_video_frame)
        self.cameraStreamThread.finished.connect(self.on_thread_finished)
        self.cameraStreamThread.start()

        self.WIFIIconThread = WIFIIconThread.WIFIIconThread()
        self.WIFIIconThread.change_icon.connect(self.change_icon)
        self.WIFIIconThread.start()

    def update_video_frame(self, qImg):
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.image_cam.setPixmap(pixmap)
        self.image_cam.setScaledContents(True)

    def change_icon(self, pixmap):
        self.image_wifi.setPixmap(pixmap)
        self.image_wifi.setScaledContents(True)

    def on_thread_finished(self):
        print("Camera stream thread finished")

    def mousePressEvent(self, event):
        super().mousePressEvent(event)

    def closeEvent(self, event):
        self.cameraStreamThread.stop()
        self.cameraStreamThread.wait()
        event.accept()
        if self.parent():
            self.parent().tWindow = None
