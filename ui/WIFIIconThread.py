import time
import os
import subprocess
import re
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal


class WIFIIconThread(QThread):
    change_icon = pyqtSignal(QtGui.QPixmap)

    def __init__(self):
        super().__init__()
        self._is_running = True  # 종료 플래그
        self.WIFI_icons = []

        # 이미지 파일 로드
        image_names = [
            "./image/wifi_good.png",
            "./image/wifi_fine.png",
            "./image/wifi_bad.png",
        ]
        for name in image_names:
            image_path = os.path.join(os.getcwd(), name)  # 현재 작업 디렉토리 기준 경로
            if os.path.exists(image_path):
                pixmap = QtGui.QPixmap(image_path)
                self.WIFI_icons.append(pixmap)
            else:
                print(f"Error: Wi-Fi 아이콘 파일을 찾을 수 없습니다: {image_path}")

    def run(self):
        while self._is_running:
            signal_strength = self.get_wifi_signal_strength()
            if not self._is_running:
                break
            if signal_strength is not None:
                if signal_strength >= -50:
                    self.change_icon.emit(self.WIFI_icons[0])
                elif signal_strength >= -70:
                    self.change_icon.emit(self.WIFI_icons[1])
                else: 
                    self.change_icon.emit(self.WIFI_icons[2])
            else:
                self.change_icon.emit(None)
            time.sleep(1)

    def stop(self):
        """스레드 종료 요청"""
        self._is_running = False

    def get_wifi_signal_strength(self):
        try:
            output = subprocess.check_output(['iwconfig', 'wlan0']).decode('utf-8')
            match = re.search(r'Signal level=(-\d+) dBm', output)
            if match:
                return int(match.group(1))
            else:
                return None
        except subprocess.CalledProcessError:
            return None