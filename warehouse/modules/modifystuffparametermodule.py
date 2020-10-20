# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot, QDate

from warehouse.views.modifystuffparmeter import Ui_Dialog

from labrecord.controllers.labrecordscontroller import LabrecordsController
from stuff.controllers.stuffcontroller import StuffController
from warehouse.controllers.warehousecontroller import WarehouseController
from supplyer.modules.selectstuffModule import SelectstuffModule

from lib.utils.messagebox import MessageBox

import decimal

import re

import user

import datetime
import re


class ModifyStuffParmeter(QDialog, Ui_Dialog):

    def __init__(self, autoid, parent=None):
        super(ModifyStuffParmeter, self).__init__(parent)
        self.ori_detail = dict()
        self.detail = {}
        self.new_detail = dict()
        self.WC = WarehouseController()
        self.SFC = StuffController()
        self.setupUi(self)

        self.autoid = autoid

        self.get_detail()
        self.set_validator()
        self.get_location_list()

    def get_detail(self):
        if not self.autoid:
            self.pushButton_accept.setEnabled(False)
            return
        key_dict = {
            'autoid': self.autoid
        }
        res = self.WC.get_stuffrepository(
            False, *VALUES_TUPLE_STUFF, **key_dict
        )
        if len(res) != 1:
            return
        self.ori_detail = res[0]
        self.lineEdit_content.setText(str(self.ori_detail['content']))
        self.label_contentunit.setText(self.ori_detail['cunit'])
        self.lineEdit_water.setText(str(self.ori_detail['water']))
        self.lineEdit_rdensity.setText(str(self.ori_detail['rdensity']))
        self.lineEdit_impurity.setText(str(self.ori_detail['impurity']))

    def set_validator(self):
        doubleValitor = QDoubleValidator()
        doubleValitor.setBottom(-1)
        doubleValitor.setDecimals(3)
        doubleValitor.setNotation(QDoubleValidator.StandardNotation)
        self.lineEdit_content.setValidator(doubleValitor)
        self.lineEdit_water.setValidator(doubleValitor)
        self.lineEdit_rdensity.setValidator(doubleValitor)
        self.lineEdit_impurity.setValidator(doubleValitor)

    def get_location_list(self):
        location_list = self.WC.get_stuffrepository(
            True, *VALUES_TUPLE_LOCATION).distinct()
        if len(location_list):
            self.comboBox_location.addItems(location_list)
        if len(self.ori_detail):
            self.comboBox_location.setCurrentText(self.ori_detail['position'])
        else:
            self.comboBox_location.setCurrentText("")

    @pyqtSlot(str)
    def on_lineEdit_content_textChanged(self, p_str):
        if p_str != '':
            p_str = decimal.Decimal(p_str)
        else:
            p_str = decimal.Decimal(-1)
        try:
            if p_str != self.ori_detail['content']:
                self.new_detail['content'] = p_str
            else:
                try:
                    del self.new_detail['content']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['content'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_water_textChanged(self, p_str):
        if p_str != '':
            p_str = decimal.Decimal(p_str)
        else:
            p_str = decimal.Decimal(p_str)
        try:
            if p_str != self.ori_detail['water']:
                self.new_detail['water'] = p_str
            else:
                try:
                    del self.new_detail['water']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['water'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_rdensity_textChanged(self, p_str):
        if p_str != '':
            p_str = decimal.Decimal(p_str)
        else:
            p_str = decimal.Decimal(p_str)
        try:
            if p_str != self.ori_detail['rdensity']:
                self.new_detail['rdensity'] = p_str
            else:
                try:
                    del self.new_detail['rdensity']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['rdensity'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_impurity_textChanged(self, p_str):
        if p_str != '':
            p_str = decimal.Decimal(p_str)
        else:
            p_str = decimal.Decimal(p_str)
        try:
            if p_str != self.ori_detail['impurity']:
                self.new_detail['impurity'] = p_str
            else:
                try:
                    del self.new_detail['impurity']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['impurity'] = p_str

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

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if len(self.new_detail):
            self.WC.update_stuffrepository(self.autoid, **self.new_detail)
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()


VALUES_TUPLE_STUFF = (
    'cunit', 'kind', 'stufftype', 'allowno', 'countercheckdays',
    'spamount', 'spunit', 'basicamount'
)

VALUES_TUPLE_LOCATION = ('position',)

VALUES_TUPLE_LAB = ('labvalue', 'putintype')

VALUES_TUPLE_STUFF = (
    "content", "cunit", "water", "rdensity", "impurity", "position"
)
