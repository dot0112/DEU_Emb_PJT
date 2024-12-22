
import os
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from main_ui import Ui_MainWindow
from WIFIIconThread import WIFIIconThread
import translateWindow

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # main_ui.py의 UI 초기화

        # 투명 배경 설정
        self.setAttribute(Qt.WA_TranslucentBackground)

        # Wi-Fi 아이콘 업데이트 스레드 설정
        self.WIFIIconThread = WIFIIconThread()
        self.WIFIIconThread.change_icon.connect(self.change_icon)
        self.WIFIIconThread.start()

        # 번역 창 초기화
        self.tWindow = None

    def change_icon(self, pixmap: QPixmap):
        """
        Wi-Fi 상태 아이콘 업데이트.
        """
        try:
            self.image_wifi.setPixmap(pixmap)
            self.image_wifi.setScaledContents(True)
        except AttributeError:
            print("Wi-Fi 아이콘 위젯(image_wifi)이 정의되지 않았습니다.")

    def showTranslateWindow(self):
        """
        번역 창 표시. 창이 이미 열려 있으면 새로 열지 않음.
        """
        if not self.tWindow:
            self.tWindow = translateWindow.TranslateWindow(self)
            self.tWindow.show()

    def mousePressEvent(self, event):
        """
        마우스 클릭 이벤트로 번역 창 표시.
        """
        self.showTranslateWindow()

    def closeEvent(self, event):
        """
        창이 닫힐 때 Wi-Fi 스레드를 종료.
        """
        if hasattr(self, 'WIFIIconThread') and self.WIFIIconThread.isRunning():
            self.WIFIIconThread.stop()  # 스레드 종료 요청
            self.WIFIIconThread.wait()  # 스레드가 종료될 때까지 대기
        event.accept()  # 이벤트 처리 완료
