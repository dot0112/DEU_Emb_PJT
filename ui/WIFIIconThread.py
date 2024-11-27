import time
import cv2
import subprocess
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal
from wifi import Cell


class WIFIIconThread(QThread):
    change_icon = pyqtSignal(QtGui.QPixmap)
    is_init = False  # 클래스 변수로 초기화 상태를 관리
    WIFI_icons = []  # 클래스 변수로 아이콘 저장

    def __init__(self):
        super().__init__()

        # 클래스 변수가 초기화되지 않은 경우에만 이미지 로딩
        if not WIFIIconThread.is_init:
            image_names = ["wifi_good.png", "wifi_fine.png", "wifi_bad.png"]
            for name in image_names:
                img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)

                qImg = QtGui.QImage(
                    img.data,
                    img.shape[1],
                    img.shape[0],
                    img.shape[1] * 4,
                    QtGui.QImage.Format_RGBA8888,
                )

                pixmap = QtGui.QPixmap.fromImage(qImg)
                WIFIIconThread.WIFI_icons.append(pixmap)

            WIFIIconThread.is_init = True  # 초기화 완료 플래그 설정

    def run(self):
        while True:  # 무한 루프를 사용하여 주기적으로 확인
            flag = 2

            try:
                output = subprocess.check_output(["iwgetid", "-r"])
                ssid = output.decode().strip()
                cells = Cell.all("wlan0")
                for cell in cells:
                    if cell.ssid == ssid:
                        signal = cell.signal  # 첫 번째 셀의 신호 강도 가져오기
                        if signal >= -50:
                            flag = 0  # 좋은 신호
                        elif signal >= -70:
                            flag = 1  # 보통 신호

            except Exception as e:
                print(f"Error: {e}")
                flag = 2

            self.change_icon.emit(WIFIIconThread.WIFI_icons[flag])
            time.sleep(1)  # 1초 간격으로 반복
