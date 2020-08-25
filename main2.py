import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets


from hashlib import md5
from functools import partial

from menu.controllers.menu import Menu

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainmenu = Menu()
    mainmenu.show()
    sys.exit(app.exec_())
