# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot, QDate

from supplyer.views.editpurstuff import Ui_Dialog

from supplyer.controllers.supplyercontroller import SupplyerController
from stuff.controllers.stuffcontroller import StuffController
from supplyer.modules.selectstuffModule import SelectstuffModule

from lib.utils.messagebox import MessageBox

import user

import datetime
import re


class EditpurstuffModule(QDialog, Ui_Dialog):

    def __init__(self, spid, ppid=None, autoid=None, parent=None):
        super(EditpurstuffModule, self).__init__(parent)
        self.ori_detail = dict()
        self.new_detail = dict()
        self.SC = SupplyerController()
        self.SFC = StuffController()
        self.setupUi(self)
        # row = ('autoid', 'stuffid', 'stuffname', 'spec', 'package')
        # key = ('stuffid', 'stuffname', 'stuffkind', 'inputcode')
        # row_name = ('id', '物料编号', '物料名称', '含量规格', '包装规格')
        # self.lineEdit_supplyer.setup('Supplyer', row, key, row_name, 539, 240)

        self.autoid = autoid
        self.spid = spid
        self.ppid = ppid

        self.get_detail()
        self.set_amount_validator()

    def get_detail(self):
        if not self.autoid:
            return
        key_dict = {
            'autoid': self.autoid
        }
        res = self.SC.get_purchstuff(False, *VALUES_TUPLE_PPLIST, **key_dict)
        if len(res) != 1:
            return
        self.ori_detail = res[0]
        self.lineEdit_stuff.setText(
            self.ori_detail['stuffid'] + ' ' + self.ori_detail['stuffname']
        )
        self.label_spec.setSign(self.ori_detail['spec'])
        self.label_package.setText(self.ori_detail['package'])
        self.lineEdit_amount.setText(str(self.ori_detail['amount']))
        self.label_unit.setText(self.ori_detail['unit'])

    def set_amount_validator(self):
        doubleValitor = QDoubleValidator()
        doubleValitor.setBottom(0)
        doubleValitor.setDecimals(3)
        doubleValitor.setNotation(QDoubleValidator.StandardNotation)
        self.lineEdit_amount.setValidator(doubleValitor)

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
        self.new_detail['stuffid'] = stuff['stuffid']
        self.new_detail['stuffname'] = stuff['stuffname']
        self.new_detail['spec'] = stuff['spec']
        self.new_detail['package'] = stuff['package']
        self.new_detail['unit'] = stuff['spunit']
        self.new_detail['stufftype'] = stuff['stufftype']
        self.lineEdit_amount.setFocus()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        text = ''
        if self.lineEdit_stuff.text() == '':
            text = "物料不能为空!\n"
        if self.lineEdit_amount.text() in ('', '0'):
            text += "采购数量不能为空!\n"
        if len(text) > 0:
            message = MessageBox(
                self, text="以下信息填写错误",
                informative=text
            )
            message.show()
            return
        if len(self.new_detail):
            if self.ppid:
                self.new_detail['ppid'] = self.ppid
            res = self.SC.update_purchstuff(self.autoid, **self.new_detail)
            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLE_PAPERNO = ('paperno',)

VALUES_TUPLE_PPLIST = (
    "autoid", "stuffid", "stuffname", "spec", "package",
    "unit", "amount", "arrivedamount"
)
VALUES_TUPLE_STUFF = (
    'stuffid', 'stuffname', 'stufftype', 'spec', 'package', 'spunit'
)
