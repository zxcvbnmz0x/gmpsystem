#coding:utf-8

from PyQt5 import QtWidgets, QtCore, QtGui


class AeroButton(QtWidgets.QPushButton):
    def __init__(self, a='images/1229014.png', b=[0,0], c=[0,0], parent=None):
        super(AeroButton, self).__init__(parent)
        #self.setEnabled(True)
        self.a = a
        self.b = b
        self.c = c
        self.hovered = False
        self.pressed = False
        self.color = QtGui.QColor(QtCore.Qt.gray)
        self.hightlight = QtGui.QColor(QtCore.Qt.lightGray)
        self.shadow = QtGui.QColor(QtCore.Qt.black)
        self.opacity = 1.0
        self.roundness = 0

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        if (self.isEnabled()):
            if self.hovered:
                self.color = self.hightlight.darker(250)
            else:
                self.color = QtGui.QColor(50, 50, 50)

        button_rect = QtCore.QRect(self.geometry())
        painter.setPen(QtGui.QPen(QtGui.QBrush(QtCore.Qt.red),2.0))
        painter_path = QtGui.QPainterPath()
        #painter_path.addRoundedRect(1, 1, button_rect.width() - 2, button_rect.height() - 2, self.roundness, self.roundness)
        painter_path.addEllipse(1, 1, button_rect.width()-2, button_rect.height()-2)
        painter.setClipPath(painter_path)
        if self.isEnabled():
            if (self.pressed == False and self.hovered == False):
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect,icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QtGui.QPixmap(QtGui.QIcon(self.a).pixmap(icon_size)))
            elif (self.hovered == True and self.pressed == False):
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect,icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QtGui.QPixmap(QtGui.QIcon(self.b).pixmap(icon_size)))
            elif self.pressed == True:
                icon_size = self.iconSize()
                icon_position = self.calculateIconPosition(button_rect,icon_size)
                painter.setOpacity(1.0)
                painter.drawPixmap(icon_position, QtGui.QPixmap(QtGui.QIcon(self.c).pixmap(icon_size)))
        else:
            icon_size = self.iconSize()
            icon_position = self.calculateIconPosition(button_rect,icon_size)
            painter.setOpacity(1.0)
            painter.drawPixmap(icon_position, QtGui.QPixmap(QtGui.QIcon(self.a).pixmap(icon_size)))

    def enterEvent(self, event):
        self.hovered = True
        self.repaint()
        QtWidgets.QPushButton.enterEvent(self,event)

    def leaveEvent(self,event):
        self.hovered = False;
        self.repaint()
        QtWidgets.QPushButton.leaveEvent(self, event)

    def mousePressEvent(self, event):
        self.pressed = True
        self.repaint()
        QtWidgets.QPushButton.mousePressEvent(self, event)

    def mouseReleaseEvent(self, event):
        self.pressed = False
        self.repaint()
        QtWidgets.QPushButton.mouseReleaseEvent(self,event)

    def calculateIconPosition(self,button_rect,icon_size):
        x = (button_rect.width() / 2) - (icon_size.width() / 2)
        y = (button_rect.height() / 2) - (icon_size.height() / 2)
        width = icon_size.width()
        height = icon_size.height()
        icon_position = QtCore.QRect()
        icon_position.setX(x)
        icon_position.setY(y)
        icon_position.setWidth(width)
        icon_position.setHeight(height)
        return icon_position