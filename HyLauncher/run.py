
import sys
import os
from PyQt5 import QtWidgets


p = os.path.join(os.getcwd(), 'app', 'utils')
if not p in sys.path:
    sys.path.append(p)

from app.main import MainWindow

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
