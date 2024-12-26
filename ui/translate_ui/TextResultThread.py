# TextResultThread.py
import time
from PyQt5.QtCore import QThread, pyqtSignal
from gtts import gTTS
import pygame
import os


class TextResultThread(QThread):
    """
    텍스트를 음성으로 변환하여 재생하는 스레드입니다.
    """

    finished = pyqtSignal()  # 작업 완료 시 시그널

    def __init__(self, textList, parent=None):
        super().__init__(parent)
        self.textList = textList.copy()

    def run(self):
        """
        텍스트를 음성으로 변환하고 재생하는 작업을 실행합니다.
        """
        self.text_to_speech(self.textList)
        self.finished.emit()  # 작업 완료 후 시그널 방출

    def text_to_speech(self, text):
        """
        주어진 텍스트를 음성으로 변환하고 재생합니다.
        """
        for text in self.textList:
            if text == "":
                continue
            try:
                # gTTS를 사용하여 텍스트를 음성으로 변환
                tts = gTTS(text, lang="ko")  # 한국어로 설정
                tts.save("output.mp3")  # mp3 파일로 저장

                # pygame을 사용하여 mp3 파일을 재생
                pygame.mixer.init()
                pygame.mixer.music.load("output.mp3")
                pygame.mixer.music.play()

                # 음성 재생이 끝날 때까지 기다립니다.
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)  # 음성 재생 중 대기

            except Exception as e:
                print(f"음성 출력 중 오류 발생: {e}")
                # 오류가 발생한 경우, 로그를 출력하거나 처리할 수 있습니다.
