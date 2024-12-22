# import cameraStreamThread
# import WIFIIconThread
# from translate_ui import Ui_TranslateWindow  # translate_ui.py에서 Ui_TranslateWindow를 임포트
# from PyQt5 import QtGui
# from PyQt5.QtWidgets import QMainWindow
# from PyQt5.QtCore import Qt


# class TranslateWindow(QMainWindow, Ui_TranslateWindow):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.setupUi(self)  # translate_ui.py의 UI 초기화

#         # 완전 투명 배경 설정
#         self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

#         # 카메라 스트림 스레드 설정
#         self.cameraStreamThread = cameraStreamThread.CameraStreamThread()
#         self.cameraStreamThread.update_frame.connect(self.update_video_frame)
#         self.cameraStreamThread.finished.connect(self.on_thread_finished)
#         self.cameraStreamThread.start()

#         # Wi-Fi 아이콘 업데이트 스레드 설정
#         self.WIFIIconThread = WIFIIconThread.WIFIIconThread()
#         self.WIFIIconThread.change_icon.connect(self.change_icon)
#         self.WIFIIconThread.start()

#     def update_video_frame(self, qImg):
#         """
#         카메라에서 받은 프레임을 UI에 업데이트.
#         """
#         pixmap = QtGui.QPixmap.fromImage(qImg)
#         self.image_cam.setPixmap(pixmap)
#         self.image_cam.setScaledContents(True)

#     def change_icon(self, pixmap):
#         """
#         Wi-Fi 상태 아이콘 업데이트.
#         """
#         self.image_wifi.setPixmap(pixmap)
#         self.image_wifi.setScaledContents(True)

#     def on_thread_finished(self):
#         """
#         카메라 스트림 스레드 종료 시 호출.
#         """
#         print("Camera stream thread finished")

#     def mousePressEvent(self, event):
#         """
#         마우스 클릭 이벤트 처리.
#         """
#         super().mousePressEvent(event)

#     def closeEvent(self, event):
#         """
#         창이 닫힐 때 스레드 정리.
#         """
#         # 카메라 스트림 스레드 종료
#         self.cameraStreamThread.stop()
#         self.cameraStreamThread.wait()

#         # 부모 윈도우의 tWindow 참조 제거
#         event.accept()
#         if self.parent():
#             self.parent().tWindow = None

import cameraStreamThread
import WIFIIconThread
import AIResultThread
from translate_ui import Ui_TranslateWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt, QTimer
import threading
import time


class TranslateWindow(QMainWindow, Ui_TranslateWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 투명 배경 설정
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # 프레임 저장 간격 제어 변수 추가
        self.last_frame_time = 0
        self.upload_time = 5000

        # 카메라 스트림 스레드 설정
        self.cameraStreamThread = cameraStreamThread.CameraStreamThread()
        self.cameraStreamThread.update_frame.connect(self.update_video_frame)
        self.cameraStreamThread.start()

        # Wi-Fi 상태 아이콘 스레드 설정
        self.WIFIIconThread = WIFIIconThread.WIFIIconThread()
        self.WIFIIconThread.change_icon.connect(self.change_icon)
        self.WIFIIconThread.start()

        # 주기적 작업 타이머 설정
        self.setup_timer()

    def update_video_frame(self, qImg):
        """
        카메라에서 받은 프레임을 UI에 업데이트하고, 이미지를 저장.
        """
        if qImg is None:
            return

        # 프레임 저장 간격 조절 (1초에 한 번만 저장)
        current_time = time.time()
        if current_time - self.last_frame_time < 1:
            qImg.save("captured_image.jpg")

        self.last_frame_time = current_time

        # 프레임 업데이트 및 이미지 저장
        pixmap = QtGui.QPixmap.fromImage(qImg)
        self.image_cam.setPixmap(pixmap)
        self.image_cam.setScaledContents(True)

    def capture_and_upload(self):
        """
        사진을 캡쳐하고 서버에 업로드한 뒤 응답 데이터를 처리.
        """
        if not self.timer.isActive():
            return

        thread = threading.Thread(
            target=AIResultThread.capture_and_upload, args=(self.resultLabel,)
        )
        thread.start()

    def setup_timer(self):
        """
        주기적으로 사진을 캡쳐하고 서버에 업로드하여 결과를 표시하는 타이머 설정.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_and_upload)
        self.timer.start(self.upload_time)  # 5초마다 실행

    def change_icon(self, pixmap):
        """
        Wi-Fi 상태 아이콘 업데이트.
        """
        self.image_wifi.setPixmap(pixmap)
        self.image_wifi.setScaledContents(True)

    def closeEvent(self, event):
        """
        창이 닫힐 때 스레드 및 타이머를 확실히 종료.
        """
        # 타이머 중지
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()

        # 카메라 스트림 스레드 종료
        if self.cameraStreamThread.isRunning():
            self.cameraStreamThread.stop()
            self.cameraStreamThread.wait()

        event.accept()
        if self.parent():
            self.parent().tWindow = None
