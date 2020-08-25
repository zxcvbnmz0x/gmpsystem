# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt


class Formwidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lineborder = list()
        self.setStyleSheet('background-color: rgb(255, 255, 0);')

    def setLineBorder(self, lineborder: list):
        self.lineborder = lineborder

    def paintEvent(self, QPaintEvent):
        if self.lineborder:
            pp = QPainter(self)
            pen = QPen()  # 定义笔格式对象
            for index, item in enumerate(self.lineborder):
                # 设置笔的宽度
                pen.setWidth(item[1])
                # 设置笔的颜色
                pen.setColor(Qt.red)
                # 将笔格式赋值给 画笔
                pp.setPen(pen)
                pp.drawRect(item[0])
