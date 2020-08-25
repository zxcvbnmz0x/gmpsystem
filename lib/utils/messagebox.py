# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QMessageBox


def MessageBox(parent=None, title="错误", icon=QMessageBox.Warning, text="",
               informative="", yes_text="确认", no_text="取消"):
    dialog = QMessageBox(parent)
    dialog.setWindowTitle(title)
    dialog.setIcon(icon)
    dialog.setText(text)
    dialog.setInformativeText(informative)
    # 添加Yes和No2个按键
    dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
    button_yes = dialog.button(QMessageBox.Yes)
    button_yes.setText(yes_text)
    button_no = dialog.button(QMessageBox.No)
    button_no.setText(no_text)
    return dialog
