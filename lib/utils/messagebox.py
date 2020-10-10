# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox, QDialog, QLabel


def MessageBox(parent=None, title="错误", icon=QMessageBox.Warning, text="",
               informative="", yes_text="确认", no_text="取消"):

    msgbox = QMessageBox(parent)
    msgbox.setWindowTitle(title)
    msgbox.setIcon(icon)
    msgbox.setText(text)
    msgbox.setInformativeText(informative)
    # 添加Yes和No2个按键
    msgbox.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    button_yes = msgbox.button(QMessageBox.Yes)
    button_yes.setText(yes_text)
    button_no = msgbox.button(QMessageBox.No)
    button_no.setText(no_text)
    return msgbox

class msgdialog(QDialog):
    def __init__(self, parent=None, title="错误", icon=QMessageBox.Warning, text="",
                   yes_text="确认", no_text="取消"):
        super(msgdialog, self).__init__(parent)
        self.resize(640,380)
        self.label = QLabel(self)
        self.label.resize(630, 370)
        self.setWindowTitle(title)
        # self.setWindowIcon(icon)
        self.label.setText(text)

    def text(self):
        return self.label.text()

    def setText(self, p_str):
        self.label.setText(p_str)