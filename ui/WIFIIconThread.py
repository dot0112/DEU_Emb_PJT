
import time
import os
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal


class WIFIIconThread(QThread):
    change_icon = pyqtSignal(QtGui.QPixmap)

    def __init__(self):
        super().__init__()
        self._is_running = True  # 종료 플래그
        self.WIFI_icons = []

        # 이미지 파일 로드
        image_names = ["wifi_good.png", "wifi_fine.png", "wifi_bad.png"]
        for name in image_names:
            image_path = os.path.join(os.getcwd(), name)  # 현재 작업 디렉토리 기준 경로
            if os.path.exists(image_path):
                pixmap = QtGui.QPixmap(image_path)
                self.WIFI_icons.append(pixmap)
            else:
                print(f"Error: Wi-Fi 아이콘 파일을 찾을 수 없습니다: {image_path}")

    def run(self):
        while self._is_running:
            for icon in self.WIFI_icons:
                if not self._is_running:
                    break
                self.change_icon.emit(icon)
                time.sleep(1)  # 1초 대기

    def stop(self):
        """스레드 종료 요청"""
        self._is_running = False