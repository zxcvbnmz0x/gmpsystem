# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, QtCore


class myLineEdit(QtWidgets.QLineEdit):
    sendmsg = QtCore.pyqtSignal(object)
    acceptmsg = QtCore.pyqtSignal()
    # 标记是否为正确的内容，0为修改过，1为正确选择
    flat = 0

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e):
        if e.key() == 16777235 or e.key() == 16777237:
            self.sendmsg.emit(e)
        else:
            QtWidgets.QLineEdit.keyPressEvent(self, e)

    def focusOutEvent(self, e):
        self.acceptmsg.emit()
        QtWidgets.QLineEdit.focusOutEvent(self, e)

    def setGeo(self, *__args):
        QtWidgets.QLineEdits.setGeometry(*__args)
