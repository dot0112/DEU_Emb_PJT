import translateWindow
import WIFIIconThread
from PyQt5 import uic, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("main.ui", self)

        self.setAttribute(Qt.WA_TranslucentBackground)

        self.WIFIIconThread = WIFIIconThread.WIFIIconThread()
        self.WIFIIconThread.change_icon.connect(self.change_icon)
        self.WIFIIconThread.start()

        self.tWindow = None

    def change_icon(self, pixmap):
        self.image_wifi.setPixmap(pixmap)
        self.image_wifi.setScaledContents(True)

    def showTranslateWindow(self):
        if not self.tWindow:
            self.tWindow = translateWindow.TranslateWindow(self)
            self.tWindow.show()

    # def closeEvent(self, event):  # 창 닫기 이벤트 처리
    #     self.WIFIIconThread.quit()  # 스레드 종료 요청
    #     self.WIFIIconThread.wait()  # 스레드가 종료될 때까지 대기
    #     event.accept()  # 이벤트 처리 완료

    def mousePressEvent(self, event):
        self.showTranslateWindow()
