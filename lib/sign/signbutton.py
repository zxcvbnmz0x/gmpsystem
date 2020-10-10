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
        self.setMinimumSize(QSize(130, 34))
        self.clicked.connect(self.open_sign)
        self.SM.userchanged.connect(self.setSign)

    def setEnabled(self, p_bool):
        if not p_bool:
            self.setStyleSheet(
                "SignButton{background-color: rgba(255, 0, 0, 0);border:none;}"
            )
        super(SignButton, self).setEnabled(p_bool)

    def open_sign(self):
        if len(self.text()):
            self.SM.username.setText(self.text())
        else:
            self.SM.username.clear()
        self.SM.exec()
    
    def setText(self, p_str):
        if p_str == ' ':
            return 
        super(SignButton, self).setText(p_str)
        
    def setSign(self, p_str):
        self.signChanged.emit(p_str)
        if p_str == ' ':
            return 
        self.setText(p_str)
