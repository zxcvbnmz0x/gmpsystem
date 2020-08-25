# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from decimal import Decimal

from warehouse.views.modifydrawamount import Ui_Dialog


class ModifyDrawamountModule(QDialog, Ui_Dialog):
    modified = pyqtSignal(Decimal)

    def __init__(self, item, parent=None):
        super(ModifyDrawamountModule, self).__init__(parent)
        self.item = item
        self.setupUi(self)
        self.setup_data(item)
        self.set_valitor()

    # 初始化内容
    def setup_data(self, item):
        if type(item) == dict:
            self.label_stuff.setText(item['stuffid'] + ' ' + item['stuffname'])
            self.label_batchno.setText(item['batchno'])
            self.label_amount.setText(str(item['amount']) + item['basicunit'])
            self.lineEdit_drawamount.setText(str(item['drawamount']))
            self.label_unit.setText(item['basicunit'])

    # 设置输入框的输入模式，只能设置浮点数
    # 范围为0~剩余库存数
    def set_valitor(self):
        doublevalitor = QDoubleValidator()
        try:
            doublevalitor.setRange(0, self.item['amount'], 4)
        except KeyError:
            pass
        doublevalitor.setNotation(QDoubleValidator.StandardNotation)
        self.lineEdit_drawamount.setValidator(doublevalitor)

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        drawamount = Decimal(str(self.lineEdit_drawamount.text()))
        self.modified.emit(drawamount)
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()
