from .CameraStreamThread import CameraStreamThread
from WIFIIconThread import WIFIIconThread
from .AIResultThread import AIResultThread
from .TextResultThread import TextResultThread
from .translate_ui import Ui_TranslateWindow
from PIRSensorThread import PIRSensorThread
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import QTimer, Qt
import threading
import time
import requests
import atexit
import traceback
import os
import pygame
from collections import deque
from gtts import gTTS


server_address = "113.198.233.233"


class TranslateWindow(QMainWindow, Ui_TranslateWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        # 투명 배경 설정
        self.setStyleSheet("background-color: rgba(255, 255, 255, 0);")

        # 프레임 저장 간격 제어 변수 추가
        self.last_frame_time = 0
        self.upload_time = 2000
        self.char_queue = deque()
        self.translated_string = ["", ""]
        self.ai_thread = None

        # 카메라 스트림 스레드 설정
        self.cameraStreamThread = CameraStreamThread()
        self.cameraStreamThread.update_frame.connect(self.update_video_frame)
        self.cameraStreamThread.start()

        # Wi-Fi 상태 아이콘 스레드 설정
        self.WIFIIconThread = WIFIIconThread()
        self.WIFIIconThread.change_icon.connect(self.change_icon)
        self.WIFIIconThread.start()

        self.stop_event = threading.Event()
        self.queue_thread = threading.Thread(target=self.monitor_char_queue)
        self.queue_thread.daemon = True
        self.queue_thread.start()

        self.pir_thread = PIRSensorThread()
        self.pir_thread.motion_undetected.connect(self.close)
        self.pir_thread.start()

        self.showFullScreen()

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

        self.ai_thread = AIResultThread(self.char_queue)
        self.ai_thread.result_ready.connect(self.handle_result)
        self.ai_thread.error_occurred.connect(self.handle_error)
        self.ai_thread.start()

    def handle_result(self, result):
        print("결과:", result)
        # 여기에서 결과를 처리합니다.

    def handle_error(self, error_message):
        print("에러:", error_message)
        # 여기에서 에러를 처리합니다.

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
                if not self.isVisible():
                    return
                self.process_char_data()

        time.sleep(1.0)

    def set_result_label(self):
        result_string = ""
        result_string += (
            self.translated_string[0] + " " + self.translated_string[1] + " "
        )
        char_queue_copy = list(self.char_queue)
        for c in char_queue_copy:
            result_string += c
        self.resultLabel.setText(result_string)

    def start_text_result_thread(self, textList):
        """
        TextResultThread를 실행하여 음성 출력을 처리합니다.
        """
        self.text_thread = TextResultThread(textList)
        self.text_thread.finished.connect(self.on_text_thread_finished)
        self.text_thread.start()

    def on_text_thread_finished(self):
        """
        TextResultThread 작업 완료 후 호출됩니다.
        """
        # 스레드 메모리 해제
        if self.text_thread is not None:
            self.text_thread.deleteLater()
            self.text_thread = None

    def process_char_data(self):
        if len(self.char_queue) >= 10:
            sending_string = self.translated_string[0] + self.translated_string[1]
            for c in self.char_queue:
                sending_string += c
            self.char_queue.clear()
            url = f"http://{server_address}:3000/translate/text"

            try:
                data = {"korean_text": sending_string}
                headers = {"Content-Type": "application/json"}
                response = requests.post(url, json=data, headers=headers, timeout=10)
                response.raise_for_status()
                if response.status_code == 200:
                    print(response.json())
                    translated_text = response.json()["translated_text"]
                    split_text = translated_text.split("/")
                    for i, text in enumerate(reversed(split_text[:-1])):
                        if i >= 2:
                            break
                        self.translated_string[1 - i] = text
                    self.start_text_result_thread(self.translated_string)
            except requests.exceptions.RequestException as e:
                print(f"오류 발생: {str(e)}")

        self.set_result_label()

    def closeEvent(self, event):
        # 타이머 중지
        if hasattr(self, "timer"):
            try:
                if self.timer.isActive():
                    self.timer.stop()
                self.timer.deleteLater()
            except RuntimeError:
                # 타이머가 이미 삭제된 경우 처리
                pass

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

    def keyPressEvent(self, e):
        key = e.key()
        korean_key = self.map_to_korean(key)
        if korean_key is not None:
            if korean_key == "b":
                if len(self.char_queue) > 0:
                    self.char_queue.pop()
            else:
                self.char_queue.append(korean_key)

    def map_to_korean(self, key):
        korean_mapping = {
            Qt.Key_A: "ㅁ",
            Qt.Key_B: "ㅠ",
            Qt.Key_C: "ㅊ",
            Qt.Key_D: "ㅇ",
            Qt.Key_E: "ㄷ",
            Qt.Key_F: "ㄹ",
            Qt.Key_G: "ㅎ",
            Qt.Key_H: "ㅗ",
            Qt.Key_I: "ㅑ",
            Qt.Key_J: "ㅓ",
            Qt.Key_K: "ㅏ",
            Qt.Key_L: "ㅣ",
            Qt.Key_M: "ㅡ",
            Qt.Key_N: "ㅜ",
            Qt.Key_O: "ㅐ",
            Qt.Key_P: "ㅔ",
            Qt.Key_Q: "ㅂ",
            Qt.Key_R: "ㄱ",
            Qt.Key_S: "ㄴ",
            Qt.Key_T: "ㅅ",
            Qt.Key_U: "ㅕ",
            Qt.Key_V: "ㅍ",
            Qt.Key_W: "ㅈ",
            Qt.Key_X: "ㅌ",
            Qt.Key_Y: "ㅛ",
            Qt.Key_Z: "ㅋ",
            Qt.Key_Backspace: "b",
        }
        return korean_mapping.get(key, None)
