import time, cv2
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal


class CameraStreamThread(QThread):
    update_frame = pyqtSignal(QtGui.QImage)

    def __init__(self):
        super().__init__()
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # 가로 해상도 설정
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)  # 세로 해상도 설정
        while self.running:
            ret, img = cap.read()
            if ret:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                h, w, c = img.shape
                qImg = QtGui.QImage(img.data, w, h, w * c, QtGui.QImage.Format_RGB888)
                self.update_frame.emit(qImg)
            else:
                print("Error: Cannot read frame.")
            time.sleep(0.033)
        cap.release()

    def stop(self):
        self.running = False
