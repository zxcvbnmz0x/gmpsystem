# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot, QDate

from equipment.views.editeqcheckdetail import Ui_Dialog
from equipment.controllers.equipmentcontroller import EquipmentController

import user


class EditEquCheckDetailModule(QDialog, Ui_Dialog):
    def __init__(self, autoid=None,eqid=0, parent=None):
        super(EditEquCheckDetailModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        self.eqid = eqid
        self.EC = EquipmentController()
        self.ori_detail = dict()
        self.new_detail = dict()

        self.get_detail()
        self.get_company_items()

    def get_detail(self):
        if self.autoid is None:
            self.dateEdit_checkdate.setDate(user.now_date)
            return
        key_dict = {'autoid': self.autoid}
        res = self.EC.get_data(2, False, *VALUES_TUPLE_EQCHECK, **key_dict)
        if not len(res):
            return
        self.ori_detail = res[0]
        self.dateEdit_checkdate.setDate(self.ori_detail['checkdate'])
        self.lineEdit_result.setText(self.ori_detail['result'])


    def get_company_items(self):
        items = self.EC.get_data(2, True, *VALUES_TUPLE_COMPANY).distinct()
        self.comboBox_company.addItems(items)
        if len(self.ori_detail):
            self.comboBox_company.setCurrentText(self.ori_detail['company'])
        else:
            self.comboBox_company.setCurrentText('')

    @pyqtSlot(QDate)
    def on_dateEdit_checkdate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['checkdate']) is str:
                self.new_detail['checkdate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['checkdate']):
                self.new_detail['checkdate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['checkdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['checkdate'] = q_date.toPyDate()

    @pyqtSlot(str)
    def on_comboBox_company_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['company']:
                self.new_detail['company'] = p_str
            else:
                try:
                    del self.new_detail['company']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['company'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_result_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['result']:
                self.new_detail['result'] = p_str
            else:
                try:
                    del self.new_detail['result']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['result'] = p_str

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if len(self.new_detail):
            self.new_detail['registerid'] = user.user_id
            self.new_detail['registername'] = user.user_name
            if self.autoid:
                condition = {'autoid': self.autoid}
                self.EC.update_data(2, condition, **self.new_detail)
            else:
                self.new_detail['eqid'] = self.eqid
                self.EC.update_data(2, **self.new_detail)
        self.accept()


    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

    @pyqtSlot()
    def on_pushButton_apply_clicked(self):
        self.new_detail['status'] = 1
        self.new_detail['registerid'] = user.user_id
        self.new_detail['registername'] = user.user_name
        if self.autoid:
            condition = {'autoid': self.autoid}
            self.EC.update_data(2, condition, **self.new_detail)
        else:
            self.new_detail['eqid'] = self.eqid
            self.EC.update_data(2, **self.new_detail)
        self.accept()

VALUES_TUPLE_EQCHECK = (
    'autoid', 'checkdate', 'company', 'result', 'registerid', 'registername'
)
VALUES_TUPLE_COMPANY = ('company', )
