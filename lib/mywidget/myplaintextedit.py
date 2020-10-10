# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTextEdit
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtCore import pyqtSignal, pyqtSlot


class myQrcodeEdit(QTextEdit):
    entered = pyqtSignal(QKeyEvent)
    nexted = pyqtSignal(QKeyEvent)
    focused = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

    def keyPressEvent(self, e):
        # tab 和 回车键
        if e.key()  in (16777217, 16777220):
            self.nexted.emit(e)
        else:
            super(myQrcodeEdit, self).keyPressEvent(e)

    def focusInEvent(self, e):

        self.focused.emit()
        super(myQrcodeEdit, self).focusOutEvent(e)

