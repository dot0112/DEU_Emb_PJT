from . import cameraStreamThread
import WIFIIconThread
from . import AIResultThread
from .translate_ui import Ui_TranslateWindow
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer
import threading
import time
import requests
import atexit
import traceback
from collections import deque

atexit.register(AIResultThread.executor.shutdown)


class TranslateWindow(QMainWindow, Ui_TranslateWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 투명 배경 설정
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # 프레임 저장 간격 제어 변수 추가
        self.last_frame_time = 0
        self.upload_time = 1000
        self.char_queue = deque()
        self.translated_string = ""

        # 카메라 스트림 스레드 설정
        self.cameraStreamThread = cameraStreamThread.CameraStreamThread()
        self.cameraStreamThread.update_frame.connect(self.update_video_frame)
        self.cameraStreamThread.start()

        # Wi-Fi 상태 아이콘 스레드 설정
        self.WIFIIconThread = WIFIIconThread.WIFIIconThread()
        self.WIFIIconThread.change_icon.connect(self.change_icon)
        self.WIFIIconThread.start()

        self.stop_event = threading.Event()
        self.queue_thread = threading.Thread(target=self.monitor_char_queue)
        self.queue_thread.daemon = True
        self.queue_thread.start()

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
            qImg.save("./image/captured_image.jpg")

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
            target=AIResultThread.capture_and_upload, args=(self.char_queue,)
        )
        thread.start()

    def setup_timer(self):
        """
        주기적으로 사진을 캡쳐하고 서버에 업로드하여 결과를 표시하는 타이머 설정.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.capture_and_upload)
        self.timer.setSingleShot(False)  # 반복 실행 허용
        self.timer.start(self.upload_time)  # 실행 간격 설정

    def change_icon(self, pixmap):
        """
        Wi-Fi 상태 아이콘 업데이트.
        """
        self.image_wifi.setPixmap(pixmap)
        self.image_wifi.setScaledContents(True)

    def monitor_char_queue(self):
        while not self.stop_event.is_set():
            if len(self.char_queue) != 0:
                # 창이 닫혔으면 업데이트 중단
                if not self.isVisible():
                    return
                self.process_char_data()

        time.sleep(1.0)

    def process_char_data(self):
        if len(self.char_queue) >= 6:
            sending_string = self.translated_string
            for c in self.char_queue:
                sending_string += c
            self.char_queue.clear()
            url = "http://localhost:3000/translated/text"
            try:
                data = {"korean_text": sending_string}
                response = requests.post(url, data, timeout=10)
                response.raise_for_status()
                if response.status_code == 200:
                    translated_text = response.json().translated_text
                    split_text = translated_text.split("/")
                    self.translated_string = split_text[0]
                    self.resultLabel.text = split_text[0]
                    if len(split_text) > 1:
                        self.resultLabel.text += split_text[1]
                        for c in split_text[1]:
                            self.char_queue.append(c)
            except requests.exceptions.RequestException as e:
                print(f"오류 발생: {str(e)}")
        else:
            self.resultLabel.text += self.char_queue[-1]
        # 예: UI 업데이트, 번역 수행, 다른 작업 등

    def closeEvent(self, event):
        # 타이머 중지
        if hasattr(self, "timer") and self.timer.isActive():
            self.timer.stop()
            self.timer.deleteLater()

        # 백그라운드 스레드 종료 비동기 처리
        threading.Thread(target=self.shutdown_threads).start()

        super().closeEvent(event)
        if self.parent():
            self.parent().tWindow = None
        event.accept()

    def shutdown_threads(self):
        """
        백그라운드 스레드를 안전하게 종료하고, 오류가 발생할 경우 기록.
        """
        try:
            # 카메라 스트림 스레드 종료
            if (
                hasattr(self, "cameraStreamThread")
                and self.cameraStreamThread.isRunning()
            ):
                try:
                    self.cameraStreamThread.stop()
                    self.cameraStreamThread.wait()
                except Exception as e:
                    print(f"카메라 스트림 스레드 종료 중 오류 발생: {e}")
                    traceback.print_exc()

            # WiFi 아이콘 스레드 종료
            if hasattr(self, "WIFIIconThread") and self.WIFIIconThread.isRunning():
                try:
                    self.WIFIIconThread.stop()
                    self.WIFIIconThread.wait()
                except Exception as e:
                    print(f"WiFi 아이콘 스레드 종료 중 오류 발생: {e}")
                    traceback.print_exc()

            # 큐 모니터링 스레드 종료
            if hasattr(self, "stop_event") and hasattr(self, "queue_thread"):
                try:
                    self.stop_event.set()
                    self.queue_thread.join()
                except Exception as e:
                    print(f"큐 모니터링 스레드 종료 중 오류 발생: {e}")
                    traceback.print_exc()

        except Exception as e:
            # 전체 종료 프로세스에서 발생한 예기치 않은 오류
            print(f"스레드 종료 처리 중 알 수 없는 오류 발생: {e}")
            traceback.print_exc()
