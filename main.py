import sys
from PyQt6.QtWidgets import QApplication
from menu import Menu


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)

stylesheet = """ Menu { background-image: url("fon1.jpg"); background-repeat: no-repeat; background-position: center; } """
if __name__ == '__main__':

    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    ex = Menu()
    sys.excepthook = except_hook
    ex.show()
    sys.exit(app.exec())
