# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QHeaderView, QTreeWidgetItemIterator
from PyQt5.QtGui import QDrag, QIcon
from PyQt5.QtCore import QTextStream, pyqtSignal, QMimeData, QDataStream, QByteArray, QIODevice, \
    Qt, QAbstractItemModel, QPoint

class MyTreeWidget(QTreeWidget):
    droped = pyqtSignal(str)

    keyEntered = pyqtSignal()
    def __init__(self, parent=None):
        super(MyTreeWidget, self).__init__(parent)
        self.setWordWrap(True)
        # 需要调整宽度的列
        # self.stretch_list = []
        # 显示的列数量
        # self.visable_count = 0
        # self.header().sectionResized.connect(self.on_header_sectionResized)

    def keyPressEvent(self, e):
        if e.key() == 16777220:
            self.keyEntered.emit()

    def dropEvent(self, event):
        event.accept()
        if event.mimeData().hasFormat("application/x-text"):
            data = event.mimeData().data('application/x-text')
            stream = QDataStream(data, QIODevice.ReadOnly)
            item = stream.readQString()
            self.droped.emit(item)
        else:
            event.ignore()


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-text"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-text"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("application/x-text"):
            event.setDropAction(Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def startDrag(self, QDropEvent):
        srid = self.currentItem().text(0)
        mimedata = QMimeData()
        data = QByteArray()
        stream = QDataStream(data, QIODevice.WriteOnly)
        stream.writeQString(srid)
        mimedata.setData('application/x-text', data)
        drag = QDrag(self)
        drag.setMimeData(mimedata)
        drag.exec(Qt.MoveAction)

    def hideColumns(self, *args):
        for i in args:
            self.hideColumn(i)

    def resizeColumns(self, max_len, *args):
        for i in args:
            self.resizeColumnToContents(i)
            if self.columnWidth(i) > max_len:
                # self.stretch_list.append(i)
                self.setColumnWidth(i, max_len)
        # if len(self.stretch_list):
        #     self.resetText()

    def resetText(self):
        it = QTreeWidgetItemIterator(self)
        while it.value():
            for i in self.stretch_list:
                p_str = it.value().text(i).replace('\n', '').replace('\r', '')
                width = self.columnWidth(i)
                try:
                    text = ''
                    temptext = ''
                    for letter in p_str:
                        if self.fontMetrics().width(temptext + letter) > width-10:
                            temptext += '\n'
                            text += temptext
                            temptext = letter
                        else:
                            temptext += letter
                    if len(temptext):
                        text += temptext
                except AttributeError:
                    text = p_str
                it.value().setText(i, text)
            it += 1

    def on_header_sectionResized(self, p_int, p_int_1, p_int_2):
        try:
            it = QTreeWidgetItemIterator(self)
            while it.value():
                it.value().resetText(p_int, p_int_2)
                it += 1
        except ValueError:
            pass

class MyTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent=None):
        super(MyTreeWidgetItem, self).__init__(parent)

    def resetText(self, p_int, width):
        p_str = self.text(p_int).replace('\n', '').replace('\r', '')
        try:
            text = ''
            temptext = ''
            for letter in p_str:
                if self.treeWidget().fontMetrics().width(temptext + letter) >= width-10:
                    temptext += '\n'
                    text += temptext
                    temptext = letter
                else:
                    temptext += letter
            if len(temptext):
                text += temptext
        except AttributeError:
            text = p_str
        self.setText(p_int, text)
