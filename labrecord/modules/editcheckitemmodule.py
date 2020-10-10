# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDate

from labrecord.controllers.labrecordscontroller import LabrecordsController

from labrecord.views.editcheckitem import Ui_Dialog

import user
import datetime

CHECK_RESULT = ("符合规定", "不符合规定")


class EditcheckitemModule(QDialog, Ui_Dialog):

    def __init__(self, autoid, parent=None):
        super(EditcheckitemModule, self).__init__(parent)
        self.autoid = autoid
        self.ori_detail = dict()
        self.new_detail = dict()
        self.LC = LabrecordsController()
        self.setupUi(self)

        # 获取检验项目内容
        self.get_checkitemdetail()

    def get_checkitemdetail(self):
        values_list = (
            'itemname', 'referencevalue', 'labvalue', 'result', 'startdate',
            'enddate'
        )
        key_dict = {
            'autoid': self.autoid
        }
        res = self.LC.get_labitem(False, *values_list, **key_dict)
        self.ori_detail = res[0]
        for item in res:
            self.label_itemname.setText(item['itemname'])
            self.textEdit_referencevalue.setText(item['referencevalue'])
            self.textEdit_labvalue.setText(item['labvalue'])
            self.comboBox_result.setCurrentIndex(item['result'])
            self.dateEdit_startdate.setDate(
                item['startdate'] if type(item['startdate']) is datetime.date else
                user.now_date
            )
            self.dateEdit_enddate.setDate(
                item['enddate'] if type(item['enddate']) is datetime.date else
                user.now_date
            )

    @pyqtSlot(QDate)
    def on_dateEdit_startdate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['startdate']) is str:
                self.new_detail['startdate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['startdate']):
                self.new_detail['startdate'] = q_date.toPyDate()

            else:
                try:
                    del self.new_detail['startdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['startdate'] = q_date.toPyDate()

    @pyqtSlot(QDate)
    def on_dateEdit_enddate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['enddate']) is str:
                self.new_detail['enddate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['enddate']):
                self.new_detail['enddate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['enddate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['enddate'] = q_date.toPyDate()

    @pyqtSlot(str)
    def on_textEdit_labvalue_textEdited(self, p_str):
        try:
            if p_str != self.ori_detail['labvalue']:
                self.new_detail['labvalue'] = p_str
            else:
                try:
                    del self.new_detail['labvalue']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['labvalue'] = p_str

    @pyqtSlot(int)
    def on_comboBox_result_currentIndexChanged(self, p_int):
        try:
            if p_int != self.ori_detail['result']:
                self.new_detail['result'] = p_int
            else:
                try:
                    del self.new_detail['result']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['result'] = p_int

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if len(self.new_detail):
            res = self.LC.update_labitem(self.autoid, **self.new_detail)
            print(res)
            if res:
                self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()