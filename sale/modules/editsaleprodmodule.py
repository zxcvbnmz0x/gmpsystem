# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5 .QtGui import QDoubleValidator
from PyQt5.QtCore import pyqtSlot

from sale.controllers.salecontroller import SaleController
from product.controllers.productcontroller import ProductController

from sale.views.editsaleprod import Ui_Dialog

import decimal

from lib.utils.messagebox import MessageBox


class EditSaleProdMudule(QDialog, Ui_Dialog):
    def __init__(self, autoid=None, snid=None, parent=None):
        super(EditSaleProdMudule, self).__init__(parent)
        self.setupUi(self)
        self.autoid=autoid
        self.snid = snid
        self.SC = SaleController()
        self.PC = ProductController()
        self.ori_detail = dict()
        self.new_detail = dict()
        row = ('autoid', 'prodid', 'prodname', 'spec', 'package')
        key = ('prodid', 'prodname', 'commonname', 'inputcode')
        row_name = ("id", "产品编号", "产品名称", "含量规格", "包装规格")
        self.lineEdit_product.setup('Productdictionary', row, key, row_name, 620, 190)
        self.set_validator()
        if self.autoid is not None:
            self.get_detail()

    def get_detail(self):
        key_dict = {'autoid': self.autoid}
        detail_list = self.SC.get_salenotegoods(
            False, *VALUES_TUPLE_PROD, **key_dict
        )
        if not len(detail_list):
            return
        self.ori_detail = detail_list[0]
        self.lineEdit_product.setText(
            self.ori_detail['prodid'] + ' ' + self.ori_detail['prodname']
        )
        self.label_spec.setText(self.ori_detail['spec'])
        self.label_package.setText(self.ori_detail['package'])
        self.lineEdit_amount.setText(str(self.ori_detail['saleamount'].to_integral()))
        self.label_unit.setText(self.ori_detail['spunit'])

    def set_validator(self):
        doubleValitor = QDoubleValidator()
        doubleValitor.setBottom(0)
        self.lineEdit_amount.setValidator(doubleValitor)

    @pyqtSlot(str)
    def on_lineEdit_product_textChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        key_dict = {'prodid': id, 'prodname': name}
        res = self.PC.get_product_or_stuff_dictionary(
            0, False, *VALUES_TUPLE_PRODDICT, **key_dict
        )
        if len(res):
            prod_detail = res[0]
            self.label_spec.setText(prod_detail['spec'])
            self.label_package.setText(prod_detail['package'])
            self.label_unit.setText(prod_detail['spunit'])
            try:
                if id != self.ori_detail['prodid'] or name != self.ori_detail[
                    'prodname']:
                    self.new_detail['prodid'] = id
                    self.new_detail['prodname'] = name
                    self.new_detail['spec'] = prod_detail['spec']
                    self.new_detail['package'] = prod_detail['package']
                    self.new_detail['spunit'] = prod_detail['spunit']
                else:
                    try:
                        del self.new_detail['prodid']
                        del self.new_detail['prodname']
                        del self.new_detail['spec']
                        del self.new_detail['package']
                        del self.new_detail['spunit']
                    except KeyError:
                        pass
            except KeyError:
                self.new_detail['prodid'] = id
                self.new_detail['prodname'] = name
                self.new_detail['spec'] = prod_detail['spec']
                self.new_detail['package'] = prod_detail['package']
                self.new_detail['spunit'] = prod_detail['spunit']

    @pyqtSlot(str)
    def on_lineEdit_amount_textChanged(self, p_str):

        try:
            p_num = decimal.Decimal(p_str)
            if p_num != self.ori_detail['saleamount']:
                self.new_detail['saleamount'] = p_num
            else:
                try:
                    del self.new_detail['saleamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['saleamount'] = p_num
        except decimal.InvalidOperation:
            pass

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if not len(self.new_detail):
            return
        saleamount = self.lineEdit_amount.text()
        if saleamount in ('0', ''):
            msg = MessageBox(self, text="销售数量不能为空")
            msg.show()
            return
        if self.autoid is None and self.snid is not None:
            self.new_detail['snid'] = self.snid

        self.SC.update_salenotegoods(self.autoid, **self.new_detail)
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLE_PRODDICT = ('spec', 'package', 'spunit')

VALUES_TUPLE_PROD = (
    'autoid', 'prodid', 'prodname', 'spec', 'package', 'spunit', 'saleamount'
)
