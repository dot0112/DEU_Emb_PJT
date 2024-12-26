from PyQt5.QtCore import QThread, pyqtSignal
from gpiozero import MotionSensor


class PIRSensorThread(QThread):
    motion_detected = pyqtSignal()
    motion_undetected = pyqtSignal()
    pir_sensor = MotionSensor(pin=7, queue_len=10, threshold=0.75)

    def __init__(self):
        super().__init__()
        self.endCount = 0
        self.running = True

    def run(self):
        while self.running:
            if self.pir_sensor.motion_detected:
                self.endCount = 0
                self.motion_detected.emit()
            else:
                self.endCount += 1
                if self.endCount >= 70:
                    self.motion_undetected.emit()
            self.msleep(100)  # 100ms 대기

    def stop(self):
        self.running = False
