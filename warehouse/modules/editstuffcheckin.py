# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot, QDate

from warehouse.views.editstuffcheckin import Ui_Dialog

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


class EditStuffCheckInModule(QDialog, Ui_Dialog):

    def __init__(self, autoid, lrid=0, parent=None):
        super(EditStuffCheckInModule, self).__init__(parent)
        self.ori_detail = dict()
        self.detail = {
            'content': decimal.Decimal('-1'),
            'cunit': '%',
            'water': decimal.Decimal('-1'),
            'rdensity': decimal.Decimal('-1'),
            'impurity': decimal.Decimal('-1'),
            'position': ''
        }
        self.new_detail = dict()
        self.LC = LabrecordsController()
        self.WC = WarehouseController()
        self.SFC = StuffController()
        self.setupUi(self)

        self.autoid = autoid
        self.lrid = lrid

        self.get_detail()
        if lrid != 0:
            self.set_putin_parameter()
        self.set_validator()
        self.get_location_list()
        if len(self.ori_detail):
            self.set_content_unit()

    def get_detail(self):
        if not self.autoid:
            self.pushButton_accept.setEnabled(False)
            return
        key_dict = {
            'autoid': self.autoid
        }
        res = self.WC.get_stuffcheckinlist(
            False, *VALUES_TUPLE_CHECK_IN_LIST, **key_dict
        )
        if len(res) != 1:
            return
        self.ori_detail = res[0]

    def set_putin_parameter(self):
        key_dict = {'lrid': self.lrid}
        res = self.LC.get_labitem(False, *VALUES_TUPLE_LAB, **key_dict)
        for item in res:
            if item['putintype'] == 1:
                try:
                    content = re.findall('\d+\.?\d?',item['labvalue'])[0]
                    self.lineEdit_content.setText(content)
                except IndexError:
                    pass
            elif item['putintype'] == 2:
                try:
                    water = re.findall('\d+\.?\d?',item['labvalue'])[0]
                    self.lineEdit_water.setText(water)
                except IndexError:
                    pass
            elif item['putintype'] == 3:
                try:
                    rdensity = re.findall('\d+\.?\d?',item['labvalue'])[0]
                    self.lineEdit_rdensity.setText(rdensity)
                except IndexError:
                    pass
            elif item['putintype'] == 4:
                try:
                    impuriity = re.findall('\d+\.?\d?',item['labvalue'])[0]
                    self.lineEdit_impurity.setText(impuriity)
                except IndexError:
                    pass


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
        location_list = self.WC.get_stuffcheckinlist(
            True, *VALUES_TUPLE_LOCATION).distinct()
        if len(location_list):
            self.comboBox_location.addItems(location_list)
        if len(self.ori_detail):
            self.comboBox_location.setCurrentText(self.ori_detail['position'])
        else:
            self.comboBox_location.setCurrentText("")

    def set_content_unit(self):
        cunit = '%'
        stuffid = self.ori_detail['stuffid']
        key_dict = {'stuffid': stuffid}
        stuff_list = self.SFC.get_stuffdict(
            False, *VALUES_TUPLE_STUFF, **key_dict
        )
        if len(stuff_list):
            stuff = stuff_list[0]
            cunit = stuff['cunit']
            self.label_contentunit.setText(cunit)
            self.detail['cunit'] = cunit
            self.detail['stuffkind'] = stuff['kind']
            self.detail['stufftype'] = stuff['stufftype']
            self.detail['allowno'] = stuff['allowno']
            self.detail['nextcheckdate'] = user.now_date + datetime.timedelta(
                days=stuff['countercheckdays'])
            self.detail['spamount'] = stuff['spamount']
            self.detail['spunit'] = stuff['spunit']
            self.detail['basicamount'] = stuff['basicamount']

    @pyqtSlot(str)
    def on_lineEdit_content_textChanged(self, p_str):
        self.detail['content'] = decimal.Decimal(p_str)

    @pyqtSlot(str)
    def on_lineEdit_water_textChanged(self, p_str):
        self.detail['water'] = decimal.Decimal(p_str)

    @pyqtSlot(str)
    def on_lineEdit_rdensity_textChanged(self, p_str):
        self.detail['rdensity'] = decimal.Decimal(p_str)

    @pyqtSlot(str)
    def on_lineEdit_impurity_textChanged(self, p_str):
        self.detail['impurity'] = decimal.Decimal(p_str)

    @pyqtSlot(str)
    def on_lineEdit_location_textChanged(self, p_str):
        self.detail['position'] = p_str

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):

        self.detail['ciid'] = self.ori_detail['autoid']
        self.detail['pltype'] = 0
        self.detail['stuffid'] = self.ori_detail['stuffid']
        self.detail['stuffname'] = self.ori_detail['stuffname']
        self.detail['spec'] = self.ori_detail['spec']
        self.detail['package'] = self.ori_detail['package']
        self.detail['supid'] = self.ori_detail['supid']
        self.detail['producer'] = self.ori_detail['producer']
        self.detail['makedate'] = self.ori_detail['makedate']
        self.detail['batchno'] = self.ori_detail['batchno']
        self.detail['mbatchno'] = self.ori_detail['mbatchno']
        self.detail['expireddate'] = self.ori_detail['expireddate']
        self.detail['amount'] = self.ori_detail['amount']
        self.detail['piamount'] = self.ori_detail['amount']
        self.detail['basicunit'] = self.ori_detail['unit']
        self.detail['checkindate'] = self.ori_detail['checkindate']
        self.detail['putindate'] = user.now_date
        self.detail['lrid'] = self.ori_detail['lrid']
        self.detail['warehousemanid'] = user.user_id
        self.detail['warehousemanname'] = user.user_name
        res = self.WC.update_stuffrepository(**self.detail)
        srid_id = res.autoid
        cil_detail = {
            'status': 5,
            'srid': srid_id,
            'pidate': user.now_date,
            'content': self.detail['content'],
            'cunit': self.detail['cunit'],
            'water': self.detail['water'],
            'rdensity': self.detail['rdensity'],
            'impurity': self.detail['impurity']

        }
        self.WC.update_stuffcheckinlist(self.autoid, **cil_detail)
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

VALUES_TUPLE_CHECK_IN_LIST = (
    "autoid", "stuffid", "stuffname", "spec", "package", "producer", "batchno",
    "mbatchno", "unit", "amount", "makedate", "expireddate", "position",
    "supid",
    "checkindate", "lrid"
)
