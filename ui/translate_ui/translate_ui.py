# -*- coding: utf-8 -*-

# 'translate.ui' 파일에서 생성된 폼 구현 코드
#
# PyQt5 UI 코드 생성기 5.15.11로 생성됨
#
# pyuic5를 다시 실행하면 이 파일의 수동 변경 내용이 손실될 수 있습니다. 주의하세요!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_TranslateWindow(object):
    def setupUi(self, TranslateWindow):
        # 메인 윈도우 설정
        TranslateWindow.setObjectName("TranslateWindow")
        TranslateWindow.resize(1024, 600)  # 윈도우 크기 설정

        # 중앙 위젯 설정
        self.centralwidget = QtWidgets.QWidget(TranslateWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 배경 이미지 라벨 추가 (모든 객체 아래에 위치)
        self.backgroundLabel = QtWidgets.QLabel(self.centralwidget)
        self.backgroundLabel.setGeometry(
            QtCore.QRect(0, 0, 1024, 600)
        )  # 배경 이미지가 화면 전체를 덮도록 설정
        self.backgroundLabel.setPixmap(QtGui.QPixmap("image/background.png"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setObjectName("backgroundLabel")

        # Wi-Fi 이미지 라벨 설정
        self.image_wifi = QtWidgets.QLabel(self.centralwidget)
        self.image_wifi.setGeometry(
            QtCore.QRect(930, 20, 80, 80)
        )  # 크기 조정 (50x50 -> 80x80)
        self.image_wifi.setText("")
        self.image_wifi.setObjectName("image_wifi")

        # 카메라 피드 라벨 설정
        self.image_cam = QtWidgets.QLabel(self.centralwidget)
        self.image_cam.setGeometry(QtCore.QRect(192, 70, 640, 360))  # 위치 및 크기 설정
        self.image_cam.setAlignment(QtCore.Qt.AlignCenter)  # 텍스트 가운데 정렬
        self.image_cam.setObjectName("image_cam")

        # 결과 라벨 설정
        self.resultLabel = QtWidgets.QLabel(self.centralwidget)
        self.resultLabel.setGeometry(
            QtCore.QRect(192, 440, 640, 50)
        )  # 위치 및 크기 설정
        self.resultLabel.setAlignment(QtCore.Qt.AlignCenter)  # 텍스트 가운데 정렬
        self.resultLabel.setObjectName("resultLabel")

        # 진행 상황 바 설정
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(
            QtCore.QRect(192, 510, 640, 20)
        )  # 위치 및 크기 설정
        self.progressBar.setObjectName("progressBar")

        # 메인 윈도우에 중앙 위젯 설정
        TranslateWindow.setCentralWidget(self.centralwidget)

        # 텍스트 및 스타일 재설정
        self.retranslateUi(TranslateWindow)
        QtCore.QMetaObject.connectSlotsByName(TranslateWindow)

    def retranslateUi(self, TranslateWindow):
        _translate = QtCore.QCoreApplication.translate
        # 윈도우 제목 설정
        TranslateWindow.setWindowTitle(
            _translate("TranslateWindow", "Translate Window")
        )

        # Wi-Fi 이미지 스타일 설정
        self.image_wifi.setStyleSheet(
            _translate(
                "MainWindow",
                "border: 2px solid #81D4FA; border-radius: 40px; background-color: white;",
            )
        )

        # 카메라 피드 라벨 스타일 및 텍스트 설정
        self.image_cam.setStyleSheet(
            _translate(
                "TranslateWindow",
                "border: 2px solid #A7C7E7; border-radius: 15px; background-color: #FFFFFF; font-size: 16px; color: #546E7A;",
            )
        )
        self.image_cam.setText(_translate("TranslateWindow", "Webcam Feed"))

        # 결과 라벨 스타일 및 텍스트 설정
        self.resultLabel.setStyleSheet(
            _translate(
                "TranslateWindow",
                "border: 2px dashed #C8E6C9; border-radius: 10px; padding: 10px; background-color: #FFFFFF; font-size: 20px; color: #546E7A;",
            )
        )
        self.resultLabel.setText(
            _translate("TranslateWindow", "번역 결과가 여기에 표시됩니다.")
        )

        # 진행 상황 바 스타일 설정
        self.progressBar.setStyleSheet(
            _translate(
                "TranslateWindow",
                "QProgressBar { border: 2px solid #A7C7E7; border-radius: 10px; text-align: center; color: #546E7A; background: #FFFFFF; } QProgressBar::chunk { background-color: #81D4FA; width: 10px; }",
            )
        )


if __name__ == "__main__":
    import sys

    # 애플리케이션 초기화
    app = QtWidgets.QApplication(sys.argv)

    # 메인 윈도우 객체 생성 및 설정
    TranslateWindow = QtWidgets.QMainWindow()
    ui = Ui_TranslateWindow()
    ui.setupUi(TranslateWindow)

    # 메인 윈도우 표시
    TranslateWindow.show()
    sys.exit(app.exec_())
