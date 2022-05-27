from PyQt6.QtWidgets import QApplication
import views.mainWindow as mw
import sys


def main():
    app = QApplication(sys.argv)
    window = mw.MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ =="__main__":
    main()