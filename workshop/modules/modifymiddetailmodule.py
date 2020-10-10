# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator, QIntValidator
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDateTime

from workshop.views.modifymiddetail import Ui_Dialog
from product.controllers.productcontroller import ProductController

import datetime

import user


class Modifymiddetailmodule(QDialog, Ui_Dialog):
    itemAdded = pyqtSignal()

    def __init__(self, autoid: int=0, ppid: int=0, parent=None):
        super(Modifymiddetailmodule, self).__init__(parent)
        self.autoid = autoid
        self.ppid = ppid
        self.setupUi(self)
        self.PC = ProductController()
        self.ori_detail = dict()
        self.new_detail = dict()
        # 获取当前半成品登记的详情
        self.get_detail()
        # 设置桶号的校验器
        self.set_container_validator()
        # 设置数量的校验器
        self.set_amount_validator()

    def get_detail(self):
        if not self.autoid:
            self.lineEdit_container.setText("1")
            self.dateTimeEdit_regtime.setDateTime(user.time)
            return
        values_list = [
            "container", "amount", "unit", "regtime"
        ]

        key_dict = {
            'autoid': self.autoid
        }
        res = self.PC.get_midproddrawnotes(False, *values_list, **key_dict)
        if len(res) == 1:
            self.ori_detail = res[0]
            self.lineEdit_container.setText(str(self.ori_detail['container']))
            self.lineEdit_amount.setText(str(self.ori_detail['amount']))
            self.lineEdit_unit.setText(self.ori_detail['unit'])
            self.dateTimeEdit_regtime.setDateTime(
                self.ori_detail['regtime'] if type(self.ori_detail['regtime']) \
                is datetime.datetime else user.time
            )

    def set_container_validator(self):
        intvalidator = QIntValidator()
        intvalidator.setBottom(1)
        self.lineEdit_amount.setValidator(intvalidator)

    def set_amount_validator(self):
        doublevalidator = QDoubleValidator()
        doublevalidator.setBottom(0)
        self.lineEdit_amount.setValidator(doublevalidator)

    @pyqtSlot(str)
    def on_lineEdit_container_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['container']:
                self.new_detail['container'] = p_str
            else:
                try:
                    del self.new_detail['container']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['container'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_amount_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['amount']:
                self.new_detail['amount'] = p_str
            else:
                try:
                    del self.new_detail['amount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['amount'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_unit_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['unit']:
                self.new_detail['unit'] = p_str
            else:
                try:
                    del self.new_detail['unit']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['unit'] = p_str


    @pyqtSlot(QDateTime)
    def on_dateTimeEdit_regtime_dateTimeChanged(self, q_datetime):
        try:
            if type(self.ori_detail['regtime']) is str:
                self.new_detail['regtime'] = q_datetime.toPyDateTime()
                return
            if q_datetime != QDateTime(self.ori_detail['regtime']):
                self.new_detail['regtime'] = q_datetime.toPyDateTime()
            else:
                try:
                    del self.new_detail['regtime']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['regtime'] = q_datetime.toPyDateTime()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if self.lineEdit_amount.text() == '':
            return
        if not len(self.new_detail):
            return
        self.new_detail['registrarid'] = user.user_id
        self.new_detail['registrarname'] = user.user_name

        if self.autoid:
            res = self.PC.update_midproddrawnotes(
                    autoid=self.autoid, **self.new_detail
                )
            if res:
                self.accept()
        else:
            self.new_detail['ppid'] = self.ppid
            res = self.PC.update_midproddrawnotes(**self.new_detail)
            if res:
                self.itemAdded.emit()
                container = int(self.lineEdit_container.text())
                self.lineEdit_container.setText(str(container + 1))

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()