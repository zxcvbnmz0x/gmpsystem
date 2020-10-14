# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot, QDate

from warehouse.views.editregtuff import Ui_Dialog

from supplyer.controllers.supplyercontroller import SupplyerController
from stuff.controllers.stuffcontroller import StuffController
from warehouse.controllers.warehousecontroller import WarehouseController
from supplyer.modules.selectstuffModule import SelectstuffModule

from lib.utils.messagebox import MessageBox

import user

import datetime
import re


class EditRegStuffModule(QDialog, Ui_Dialog):

    def __init__(self, spid=None, paperno=None, papertype=0, autoid=None, parent=None):
        super(EditRegStuffModule, self).__init__(parent)
        print(spid, paperno, autoid)
        self.ori_detail = dict()
        self.new_detail = dict()
        self.SC = SupplyerController()
        self.WC = WarehouseController()
        self.SFC = StuffController()
        self.setupUi(self)

        self.spid = spid
        self.autoid = autoid
        self.paperno = paperno
        self.papertype = papertype

        self.get_detail()
        self.set_amount_validator()
        self.get_producer_list()
        self.get_location_list()

    def get_detail(self):
        if not self.autoid:
            self.toolButton_more.setEnabled(True)
            return
        self.toolButton_more.setEnabled(False)
        key_dict = {
            'autoid': self.autoid
        }
        res = self.WC.get_stuffcheckinlist(
            False, *VALUES_TUPLE_CHECK_IN_LIST, **key_dict
        )
        if len(res) != 1:
            return
        self.ori_detail = res[0]
        self.lineEdit_stuff.setText(
            self.ori_detail['stuffid'] + ' ' + self.ori_detail['stuffname']
        )
        self.label_spec.setText(self.ori_detail['spec'])
        self.label_package.setText(self.ori_detail['package'])
        self.lineEdit_amount.setText(str(self.ori_detail['amount']))
        self.label_unit.setText(self.ori_detail['unit'])
        self.lineEdit_batchno.setText(self.ori_detail['batchno'])
        self.lineEdit_mbatchno.setText(self.ori_detail['mbatchno'])
        self.dateEdit_makedate.setDate(self.ori_detail['makedate'])
        self.dateEdit_invaliddate.setDate(self.ori_detail['expireddate'])

    def set_amount_validator(self):
        doubleValitor = QDoubleValidator()
        doubleValitor.setBottom(0)
        doubleValitor.setDecimals(3)
        doubleValitor.setNotation(QDoubleValidator.StandardNotation)
        self.lineEdit_amount.setValidator(doubleValitor)

    def get_location_list(self):
        location_list = self.WC.get_stuffcheckinlist(
            True, *VALUES_TUPLE_LOCATION).distinct()
        if len(location_list):
            self.comboBox_location.addItems(location_list)
        if len(self.ori_detail):
            self.comboBox_location.setCurrentText(self.ori_detail['position'])
        else:
            self.comboBox_location.setCurrentText("")

    def get_producer_list(self, sdid=None):
        if not (self.autoid or sdid):
            return
        if sdid is None:
            stuffid = self.ori_detail['stuffid']
            key_dict_stuff = {'stuffid': stuffid}
            stufffid_list = self.SFC.get_stuffdict(
                True, *VALUES_TUPLE_SDID, **key_dict_stuff
            )
            if len(stufffid_list):
                sdid = stufffid_list[0]

        if sdid and self.spid:
            key_dict_producer = {
                'sdid': sdid,
                'spid': self.spid
            }
            producer_list = self.SC.get_stuffsupplyer(
                True, *VALUES_TUPLE_PRODUCER , **key_dict_producer
            )
            if len(producer_list):
                self.comboBox_producer.addItems(producer_list)
            if len(self.ori_detail):
                self.comboBox_producer.setCurrentText(
                    self.ori_detail['producer']
                )

    @pyqtSlot(str)
    def on_lineEdit_amount_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['amount']:
                self.new_detail['amount'] = p_str
                self.new_detail['piamount'] = p_str
            else:
                try:
                    del self.new_detail['amount']
                    del self.new_detail['piamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['amount'] = p_str
            self.new_detail['piamount'] = p_str

    @pyqtSlot(str)
    def on_comboBox_producer_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['producer']:
                self.new_detail['producer'] = p_str
            else:
                try:
                    del self.new_detail['producer']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['producer'] = p_str

    @pyqtSlot(str)
    def on_comboBox_location_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['position']:
                self.new_detail['position'] = p_str
            else:
                try:
                    del self.new_detail['position']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['position'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_batchno_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['batchno']:
                self.new_detail['batchno'] = p_str
            else:
                try:
                    del self.new_detail['batchno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['batchno'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_mbatchno_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['mbatchno']:
                self.new_detail['mbatchno'] = p_str
            else:
                try:
                    del self.new_detail['mbatchno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['mbatchno'] = p_str

    @pyqtSlot(QDate)
    def on_dateEdit_makedate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['makedate']) is str:
                self.new_detail['makedate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['makedate']):
                self.new_detail['makedate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['makedate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['makedate'] = q_date.toPyDate()

    @pyqtSlot(QDate)
    def on_dateEdit_invaliddate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['expireddate']) is str:
                self.new_detail['expireddate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['expireddate']):
                self.new_detail['expireddate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['expireddate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['expireddate'] = q_date.toPyDate()

    @pyqtSlot()
    def on_toolButton_more_clicked(self):
        detail = SelectstuffModule(self.spid, self)
        detail.selected.connect(self.set_stuff)
        detail.show()

    def set_stuff(self, p_int):

        key_dict = {'autoid': p_int}
        res = self.SFC.get_stuffdict(False, *VALUES_TUPLE_STUFF, **key_dict)

        if not len(res):
            return
        stuff = res[0]
        self.lineEdit_stuff.setText(stuff['stuffid'] + stuff['stuffname'])
        self.label_spec.setText(stuff['spec'])
        self.label_package.setText(stuff['package'])
        self.label_unit.setText(stuff['spunit'])
        self.dateEdit_makedate.setDate(user.now_date)
        self.dateEdit_invaliddate.setDate(
            user.now_date + datetime.timedelta(days=stuff['expireddays'])
        )

        self.new_detail['stuffid'] = stuff['stuffid']
        self.new_detail['stuffname'] = stuff['stuffname']
        self.new_detail['spec'] = stuff['spec']
        self.new_detail['package'] = stuff['package']
        self.new_detail['unit'] = stuff['spunit']
        self.new_detail['stufftype'] = stuff['stufftype']

        self.lineEdit_batchno.setFocus()
        self.get_producer_list(p_int)

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        text = ''
        if self.lineEdit_stuff.text() == '':
            text = "物料不能为空!\n"
        if self.lineEdit_amount.text() in ('', '0'):
            text += "到货数量不能为空!\n"
        if self.lineEdit_batchno.text() == '':
            text += "进厂批号不能为空!\n"
        if len(text) > 0:
            message = MessageBox(
                self, text="以下信息填写错误",
                informative=text
            )
            message.show()
            return
        if len(self.new_detail):
            if self.spid:
                key_dict_supplyer = {'autoid': self.spid}
                supplyer_list = self.SC.get_supply(
                    False, *VALUES_TUPLE_SUPPLYER, **key_dict_supplyer
                )
                if len(supplyer_list):
                    supplyer = supplyer_list[0]
                    self.new_detail['supid'] = supplyer['supid']
                    self.new_detail['supname'] = supplyer['supname']
                self.new_detail['paperno'] = self.paperno
                self.new_detail['papertype'] = self.papertype
                self.new_detail['checkindate'] = user.now_date
            res = self.WC.update_stuffcheckinlist(self.autoid, **self.new_detail)

            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()



VALUES_TUPLE_SDID = ('autoid',)

VALUES_TUPLE_PRODUCER = ('producer',)
VALUES_TUPLE_LOCATION = ('position',)

VALUES_TUPLE_SUPPLYER = ('supid','supname')

VALUES_TUPLE_CHECK_IN_LIST = (
    "autoid", "stuffid", "stuffname", "spec", "package", "producer", "batchno",
    "mbatchno", "unit", "amount", "makedate", "expireddate", "position", "supid"
)
VALUES_TUPLE_STUFF = (
    'stuffid', 'stuffname', 'stufftype', 'spec', 'package', 'spunit',
    "expireddays"
)
