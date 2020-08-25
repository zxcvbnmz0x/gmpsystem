from PyQt5.QtWidgets import QCheckBox, QComboBox, QLineEdit, QListWidget, QCheckBox, \
    QListWidgetItem, QTreeWidget, QTreeWidgetItem
from PyQt5 import QtCore, QtWidgets


class ComboCheckBox(QComboBox):
    def __init__(self, parent=None):
        super(ComboCheckBox, self).__init__(parent)
        self.qCheckBox = []
        self.row_num = 0
        self.cbox = QCheckBox(self)
        self.cbox.move(0, 2)
        self.cbox.setTristate(False)
        self.qListWidget = QTreeWidget()
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.cbox.stateChanged.connect(self.on_cbox_toggled)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.qListWidget.setIndentation(5)
        self.qListWidget.setHeaderHidden(True)

    def on_cbox_toggled(self, p_int):
        if p_int == 2:
            for i in range(self.row_num):
                self.qCheckBox[i].setCheckState(QtCore.Qt.Checked)
        elif p_int == 0:
            for i in range(self.row_num):
                self.qCheckBox[i].setCheckState(QtCore.Qt.Unchecked)

    def setText(self, str):
        self.cbox.setText(str)

    def text(self):
        return  self.cbox.text()

    def isChecked(self):
        return self.cbox.isChecked()

    def checkState(self):
        return self.cbox.checkState()

    def selectlist(self):
        outputlist = []
        for i in range(self.row_num):
            if self.qCheckBox[i].checkState() in (1, 2):
                outputlist.append(self.qCheckBox[i].text())
        return outputlist

    def show(self):
        outputlist = self.selectlist()
        if len(outputlist) == self.row_num:
            self.cbox.setTristate(False)
            self.cbox.setCheckState(QtCore.Qt.Checked)
        elif len(outputlist) == 0:
            self.cbox.setTristate(False)
            self.cbox.setCheckState(QtCore.Qt.Unchecked)
        else:
            #self.cbox.setTristate(False)
            self.cbox.setCheckState(QtCore.Qt.PartiallyChecked)

    # 设置权限的显示文字
    # cbchbox：要添加内容的控件
    # text：要显示的内容
    def setcbchbox_name(self, chchbox, text):
        chchbox.cbox.setText(text)

    def setCheckState(self, qtstate):
        self.cbox.setCheckState(qtstate)

    # 添加权限下拉内容
    # cbchbox：要添加内容的控件
    # items：要添加的内容
    # 以下内容暂未使用，主要方法是setCheckState
    # self.qListWidget.itemClicked.connect(self.show)
    # qItem.setText(0, str(items[i]))
    # qItem.setCheckState(0, QtCore.Qt.Unchecked)
    # self.setCurrentIndex(-1)
    def setlist(self, cbchbox, q_item, items):
        if not q_item:
            q_item = self.qListWidget
        self.row_num = len(items)
        for i in range(self.row_num):
            if type(items[i]).__name__ in ("list", "dict"):
                cbbox = ComboCheckBox()
                self.qCheckBox.append(cbbox)
                qItem = QTreeWidgetItem(q_item)
                cbbox.setText(list(items[i].keys())[0])

                cbchbox.qListWidget.setItemWidget(qItem, 0, self.qCheckBox[-1])
                self.qCheckBox[-1].cbox.stateChanged.connect(self.show)
                cbbox.setlist(cbbox, cbbox.qListWidget, list(items[i].values())[0])

            else:
                self.qCheckBox.append(QCheckBox())
                qItem = QTreeWidgetItem(q_item)
                self.qCheckBox[-1].setText(items[i])
                cbchbox.qListWidget.setItemWidget(qItem, 0, self.qCheckBox[-1])
                self.qCheckBox[-1].stateChanged.connect(self.show)
