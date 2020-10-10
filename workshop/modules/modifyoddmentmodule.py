# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot, QDate

from workshop.views.modifyoddment import Ui_Dialog
from product.controllers.productcontroller import ProductController
from system.controllers.systemcontroller import SystemController

import datetime

import user


class Modifyoddmentmodule(QDialog, Ui_Dialog):
    """ 修改/增加新的零头登记记录

    """

    def __init__(self, autoid: int=0, ppid: int=0, parent=None):
        super(Modifyoddmentmodule, self).__init__(parent)
        self.autoid = autoid
        self.ppid = ppid
        self.batchno = '0'
        self.setupUi(self)
        self.PC = ProductController()
        self.SC = SystemController()
        self.ori_detail = dict()
        self.new_detail = dict()
        self.proddetail = {
            'spunit': '',
            'basicunit': ''
        }
        self.validdate = 90
        # 获取生产记录里小包装单位和基本单位
        self.get_producingplan_detail()
        # 获取当前零头登记的详情
        self.get_detail()
        # 设置数量的校验器
        self.set_amount_validator()
        # 获取零头有效期天数
        self.get_oddmentvaliddate()

    def get_producingplan_detail(self):
        values_list = (
            'spunit', 'basicunit', 'makedate'
        )
        key_dict = {
            'autoid': self.ppid
        }
        res = self.PC.get_producingplan(True, *values_list, **key_dict)
        if len(res) != 1:
            return

        self.proddetail = res[0]
        self.comboBox_unit.addItems(self.proddetail[0: 2])


    def get_detail(self):
        if not self.autoid:
            self.dateEdit_regdate.setDate(user.now_date)
            values_list = ("batchno", )

            key_dict = {
                'autoid': self.ppid
            }
            res = self.PC.get_producingplan(False, *values_list, **key_dict)
            if len(res) == 1:
                self.batchno = res[0]['batchno']
            return
        values_list = ("amount", "unit", "regdate")

        key_dict = {
            'autoid': self.autoid
        }
        res = self.PC.get_oddmentdrawnotes(False, *values_list, **key_dict)
        if len(res) == 1:
            self.ori_detail = res[0]
            self.lineEdit_amount.setText(str(self.ori_detail['amount']))
            self.comboBox_unit.setCurrentText(self.ori_detail['unit'])
            self.dateEdit_regdate.setDate(
                self.ori_detail['regdate'] if type(self.ori_detail['regdate']) \
                is datetime.datetime else user.now_date
            )

    def set_amount_validator(self):
        doublevalidator = QDoubleValidator()
        doublevalidator.setBottom(0)
        self.lineEdit_amount.setValidator(doublevalidator)

    def get_oddmentvaliddate(self):
        values_list = ('otvalue',)
        key_dict = {
            'otid': 11
        }
        res = self.SC.get_systemoption(True, *values_list, **key_dict)
        if len(res):
            self.validdate = res[0]

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
    def on_comboBox_unit_currentTextChanged(self, p_str):
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


    @pyqtSlot(QDate)
    def on_dateEdit_regdate_dateChanged(self, q_date):
        res = self.PC.get_oddment_invaliddate(
            q_date.toPyDate(), self.validdate
        )
        invaliddate = res[0]
        try:
            if type(self.ori_detail['regdate']) is str:
                self.new_detail['regdate'] = q_date.toPyDate()
                self.new_detail['invaliddate'] = invaliddate
                return
            if q_date != QDate(self.ori_detail['regdate']):
                self.new_detail['regdate'] = q_date.toPyDate()
                self.new_detail['invaliddate'] = invaliddate
            else:
                try:
                    del self.new_detail['regdate']
                    del self.new_detail['invaliddate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['regdate'] = q_date.toPyDate()
            self.new_detail['invaliddate'] = invaliddate

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if self.lineEdit_amount.text() == '':
            return
        if not len(self.new_detail):
            return
        self.new_detail['registerid'] = user.user_id
        self.new_detail['registername'] = user.user_name

        if self.autoid:
            res = self.PC.update_oddmentdrawnotes(
                    autoid=self.autoid, **self.new_detail
                )

        else:
            self.new_detail['ppid'] = self.ppid
            self.new_detail['batchno'] = self.batchno
            self.new_detail['makedate'] = self.proddetail[2]
            res = self.PC.update_oddmentdrawnotes(**self.new_detail)
        if res:
            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()