# -*- coding: utf-8 -*-

# 'main.ui' 파일에서 생성된 폼 구현 코드

# PyQt5 UI 코드 생성기 5.15.11로 생성됨

# pyuic5를 다시 실행하면 이 파일의 수동 변경 내용이 손실될 수 있습니다. 주의하세요!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        # 메인 윈도우 설정
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)

        # 중앙 위젯 설정
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Wi-Fi 이미지 라벨 설정
        self.image_wifi = QtWidgets.QLabel(self.centralwidget)
        self.image_wifi.setGeometry(
            QtCore.QRect(930, 20, 80, 80)
        )  # 크기 조정 (50x50 -> 80x80)
        self.image_wifi.setText("")
        self.image_wifi.setObjectName("image_wifi")

        # 환영 라벨 설정
        self.titleLabel = QtWidgets.QLabel(self.centralwidget)
        self.titleLabel.setGeometry(QtCore.QRect(192, 180, 640, 75))  # 위치: 중앙 근처
        self.titleLabel.setAlignment(QtCore.Qt.AlignCenter)  # 텍스트 가운데 정렬
        self.titleLabel.setObjectName("titleLabel")

        # 정보 라벨 설정
        self.infoLabel = QtWidgets.QLabel(self.centralwidget)
        self.infoLabel.setGeometry(QtCore.QRect(192, 270, 640, 50))  # 위치: 중앙 근처
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)  # 텍스트 가운데 정렬
        self.infoLabel.setObjectName("infoLabel")

        # 메인 윈도우에 중앙 위젯 설정
        MainWindow.setCentralWidget(self.centralwidget)

        # 텍스트 및 스타일 재설정
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        # 윈도우 제목 설정
        MainWindow.setWindowTitle(_translate("MainWindow", "Main Window"))

        # 중앙 위젯 스타일 설정 (배경 이미지 포함)
        self.centralwidget.setStyleSheet(
            _translate(
                "MainWindow",
                "background-image: url('image/background.png'); background-repeat: no-repeat; background-position: center; background-color: white;",
            )
        )

        # Wi-Fi 이미지 스타일 설정
        self.image_wifi.setStyleSheet(
            _translate(
                "MainWindow",
                "border: 2px solid #81D4FA; border-radius: 40px; background-color: white;",
            )
        )

        # 환영 라벨 텍스트 및 스타일 설정
        self.titleLabel.setText(_translate("MainWindow", "수화 번역기"))
        self.titleLabel.setStyleSheet(
            _translate(
                "MainWindow",
                "border: 2px solid #A7C7E7; border-radius: 10px; padding: 10px; background-color: rgba(255, 255, 255, 0.9); font-size: 50px; color: black;",
            )
        )

        # 정보 라벨 텍스트 및 스타일 설정
        self.infoLabel.setText(
            _translate("MainWindow", "번역기 가까이 오시면 자동으로 실행됩니다.")
        )
        self.infoLabel.setStyleSheet(
            _translate(
                "MainWindow",
                "border: 2px dashed #C8E6C9; border-radius: 10px; padding: 10px; background-color: rgba(255, 255, 255, 0.8); font-size: 20px; color: #546E7A;",
            )
        )


if __name__ == "__main__":
    import sys

    # 애플리케이션 초기화
    app = QtWidgets.QApplication(sys.argv)

    # 메인 윈도우 객체 생성 및 설정
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    # 메인 윈도우 표시
    MainWindow.show()
    sys.exit(app.exec_())
