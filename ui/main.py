import sys
from PyQt5.QtWidgets import QApplication
import mainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow.MainWindow()
    window.show()
    #window.showTranslateWindow()
    sys.exit(app.exec())

