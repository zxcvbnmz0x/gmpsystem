# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot

from warehouse.views.editproductputoutpaper import Ui_Dialog
from warehouse.controllers.warehousecontroller import WarehouseController


class EditProductPutOutPaperModule(QDialog, Ui_Dialog):

    def __init__(self, autoid=None, parent=None):
        super(EditProductPutOutPaperModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        self.WC = WarehouseController()
        self.ori_detail = dict()
        self.new_detail = dict()
        self.lineEdit_client.setFocus()

        if self.autoid is not None:
            self.get_detail()
        self.set_pokind()
        row = ('autoid', 'clientid', 'clientname', 'address')
        key = ('clientid', 'clientname', 'inputcode')
        row_name = ("id", "客户编号", "客户名称", "客户地址")
        self.lineEdit_client.setup('Client', row, key, row_name, 570, 200)

    def get_detail(self):
        key_dict = {
            'autoid': self.autoid
        }
        res = self.WC.get_productputoutpaper(
            False, *VALUES_TUPLE_PAPER, **key_dict
        )
        if len(res):
            self.ori_detail = res[0]
            self.lineEdit_client.setText(
                self.ori_detail['clientid'] + ' ' + self.ori_detail['clientname']
            )
            self.lineEdit_remark.setText(self.ori_detail['remark'])

    def set_pokind(self):
        res = self.WC.get_productputoutpaper(
            True, *VALUES_TUPLE_POKIND
        ).distinct()
        if len(res):
            self.comboBox_pokind.addItems(res)
        if len(self.ori_detail):
            self.comboBox_pokind.setCurrentText(self.ori_detail['pokind'])

    @pyqtSlot(str)
    def on_comboBox_pokind_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['pokind']:
                self.new_detail['pokind'] = p_str
            else:
                try:
                    del self.new_detail['pokind']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['pokind'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_client_textChanged(self, p_str):
        try:
            id ,name = p_str.split(' ')
            if id != self.ori_detail['clientid']:
                self.new_detail['clientid'] = id
                self.new_detail['clientname'] = name
            else:
                try:
                    del self.new_detail['clientid']
                    del self.new_detail['clientname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['clientid'] = id
            self.new_detail['clientname'] = name
        except ValueError:
            pass


    @pyqtSlot(str)
    def on_lineEdit_remark_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['remark']:
                self.new_detail['remark'] = p_str
            else:
                try:
                    del self.new_detail['remark']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['remark'] = p_str

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if not len(self.new_detail):
            return
        self.WC.update_productputoutpaper(self.autoid, **self.new_detail)
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLE_POKIND = ('pokind',)
VALUES_TUPLE_PAPER = ('pokind', 'clientid', 'clientname', 'remark')