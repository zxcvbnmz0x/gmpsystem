import sys
import os

from PyQt5 import QtCore, QtGui, QtWidgets


from hashlib import md5
from functools import partial

from menu.modules.menumodule import MenuModule

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainmenu = MenuModule()
    mainmenu.show()
    sys.exit(app.exec_())
