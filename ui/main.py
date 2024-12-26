import sys
from PyQt5.QtWidgets import QApplication
import main_ui.mainWindow as mainWindow
from dotenv import load_dotenv


def ExceptionHook(exctype, value, traceback):
    sys.__excepthook__(exctype, value, traceback)
    sys.exit(1)


if __name__ == "__main__":
    sys.excepthook = ExceptionHook
    load_dotenv()
    app = QApplication(sys.argv)
    window = mainWindow.MainWindow()
    window.show()
    sys.exit(app.exec())
