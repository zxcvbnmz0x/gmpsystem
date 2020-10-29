# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot

from stuff.views.editstuffreturndetail import Ui_Dialog
from stuff.controllers.stuffcontroller import StuffController

from lib.utils.messagebox import MessageBox
from lib.utils.util import to_str

import decimal

import user


class EditStuffReturnDetailModule(QDialog, Ui_Dialog):

    def __init__(self, autoid, parent=None):
        super(EditStuffReturnDetailModule, self).__init__(parent)
        self.autoid = autoid
        self.setupUi(self)
        self.SC = StuffController()
        self.ori_detail = dict()
        self.new_detail = dict()
        self.set_backamount_validator()
        self.set_pracamount_validator()
        self.set_restamount_validator()
        self.get_detail()

    def get_detail(self):
        key_dict = {'autoid': self.autoid}
        stuff_list = self.SC.get_prodstuff(
            False, *VALUE_TUPLE_STUFF, **key_dict
        )
        if not len(stuff_list):
            self.pushButton_accept.setVisible(False)
            self.pushButton_cancel.setVisible(False)
            return
        self.ori_detail = stuff_list[0]
        self.label_stuff.setText(
            self.ori_detail['stuffid'] + ' ' + self.ori_detail['stuffname']
        )
        self.label_drawamount.setText(
            to_str(self.ori_detail['drawamount']) + \
            self.ori_detail['drawunit']
        )
        self.lineEdit_pracamount.setText(
            to_str(self.ori_detail['pracamount'])
        )
        self.label_realunit.setText(self.ori_detail['drawunit'])
        self.lineEdit_restamount.setText(
            to_str(self.ori_detail['restamount'])
        )
        self.label_restunit.setText(self.ori_detail['drawunit'])
        self.lineEdit_backamount.setText(
            to_str(self.ori_detail['backamount'])
        )
        self.label_backunit.setText(self.ori_detail['drawunit'])

    def set_pracamount_validator(self):
        doublevalidator = QDoubleValidator()
        try:
            max_float = self.ori_detail['drawamount']
            doublevalidator.setRange(0, max_float)
        except KeyError:
            doublevalidator.setBottom(0)
        self.lineEdit_pracamount.setValidator(doublevalidator)


        doubleValitor = QDoubleValidator()
        doubleValitor.setRange(-360, 360)
        doubleValitor.setDecimals(2)
        doubleValitor.setNotation(QDoubleValidator.StandardNotation)

    def set_restamount_validator(self):
        doublevalidator = QDoubleValidator()
        try:
            max_float = self.ori_detail['drawamount']
            pracamount = decimal.Decimal(self.lineEdit_pracamount.text())
            doublevalidator.setRange(0, max_float - pracamount)
        except (KeyError, decimal.InvalidOperation):
            doublevalidator.setBottom(0)

        self.lineEdit_restamount.setValidator(doublevalidator)

    def set_backamount_validator(self):
        doublevalidator = QDoubleValidator()
        try:
            max_float = decimal.Decimal(self.lineEdit_restamount.text())
            doublevalidator.setRange(0, max_float)
        except decimal.InvalidOperation:
            doublevalidator.setBottom(0)
        self.lineEdit_backamount.setValidator(doublevalidator)

    @pyqtSlot(str)
    def on_lineEdit_pracamount_textChanged(self, p_str):
        try:
            p_decimal = decimal.Decimal(p_str)
        except decimal.InvalidOperation:
            p_decimal = decimal.Decimal('0')
        try:

            if p_decimal != self.ori_detail['pracamount']:
                self.new_detail['pracamount'] = p_decimal
            else:
                try:
                    del self.new_detail['pracamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['pracamount'] = p_decimal

    @pyqtSlot(str)
    def on_lineEdit_restamount_textChanged(self, p_str):
        try:
            p_decimal = decimal.Decimal(p_str)
        except decimal.InvalidOperation:
            p_decimal = decimal.Decimal('0')
        try:
            if p_decimal != self.ori_detail['restamount']:
                self.new_detail['restamount'] = p_decimal
            else:
                try:
                    del self.new_detail['restamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['restamount'] = p_decimal

    @pyqtSlot(str)
    def on_lineEdit_backamount_textChanged(self, p_str):
        try:
            p_decimal = decimal.Decimal(p_str)
        except decimal.InvalidOperation:
            p_decimal = decimal.Decimal('0')
        try:
            if p_decimal != self.ori_detail['backamount']:
                self.new_detail['backamount'] = p_decimal
            else:
                try:
                    del self.new_detail['backamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['backamount'] = p_decimal

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if not len(self.new_detail):
            return
        status, text = self.check_amount()
        if status != 0:
            msg = MessageBox(self, text=text)
            msg.show()
            return
        key_dict = {'autoid': self.autoid}
        self.new_detail['wdid'] = user.user_id
        self.new_detail['wdname'] = user.user_name
        self.SC.update_productstuff(key_dict , **self.new_detail)
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

    # 检查数量填写是否异常
    # returns i
    #   0 :没有异常
    #   1 :实用量大于领取量
    #   2 :剩余量大于领取量-实用量
    #   3 :退库量大于剩余量
    def check_amount(self):
        drawamount = self.ori_detail['drawamount']
        pracamount = decimal.Decimal(self.lineEdit_pracamount.text())
        restamount = decimal.Decimal(self.lineEdit_restamount.text())
        backamount = decimal.Decimal(self.lineEdit_backamount.text())
        if pracamount > drawamount:
            return 1, "实用量大于领取量"
        elif restamount > drawamount - pracamount:
            return 2, "剩余量大于（领取量-实用量）"
        elif backamount > restamount:
            return 3, "退库量大于剩余量"
        else:
            return 0, ""


VALUE_TUPLE_STUFF =(
    'stuffid', 'stuffname', 'drawamount', 'drawunit', 'pracamount',
    'backamount', 'restamount'
)