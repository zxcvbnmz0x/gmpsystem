# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QPushButton, QSizePolicy
from PyQt5.QtCore import QSize, pyqtSignal

from lib.sign.signmodule import SignModule


class SignButton(QPushButton):
    signChanged = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.SM = SignModule(parent)
        self.setStyleSheet(
            "SignButton{background-color: rgb(255, 0, 0);border:none;}")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Minimum)
        self.setSizePolicy(sizePolicy)
        self.setMinimumSize(QSize(130, 20))
        self.clicked.connect(self.open_sign)
        self.SM.userchanged.connect(self.sign)

    def open_sign(self):
        if len(self.text()):
            self.SM.username.setText(self.text())
        else:
            self.SM.username.clear()
        self.SM.exec()

    def sign(self, p_str):
        self.setText(p_str)
        self.signChanged.emit(p_str)
