import sys
from PyQt5.QtWidgets import QApplication
from translateWindow import TranslateWindow

def main():
    # PyQt5 애플리케이션 생성
    app = QApplication(sys.argv)

    # translateWindow 객체 생성 및 실행
    window = TranslateWindow()
    window.show()

    # PyQt5 이벤트 루프 시작
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
