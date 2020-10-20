# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog

from PyQt5.QtCore import pyqtSlot, QDate

from sale.controllers.salecontroller import SaleController

from sale.views.editsaleorder import Ui_Dialog

from lib.utils.messagebox import MessageBox

import re

import user


class EditSaleOrderMudule(QDialog, Ui_Dialog):
    def __init__(self, autoid=None, parent=None):
        super(EditSaleOrderMudule, self).__init__(parent)
        self.setupUi(self)
        self.autoid=autoid
        self.SC = SaleController()
        self.ori_detail = dict()
        self.new_detail = dict()
        row = ('autoid', 'clientid', 'clientname', 'address')
        key = ('clientid', 'clientname', 'inputcode')
        row_name = ("id", "客户编号", "客户名称", "客户地址")
        self.lineEdit_client.setup('Client', row, key, row_name, 550, 290)
        if self.autoid is None:
            self.set_paperno()
            self.dateEdit_saledate.setDate(user.now_date)
            self.dateEdit_deliverydate.setDate(user.now_date)
        else:
            self.get_detail()
        self.set_conveyance_list()
        self.set_paymethod_list()

    def get_detail(self):
        key_dict = {'autoid': self.autoid}
        detail_list = self.SC.get_salenotes(
            False, *VALUES_TUPLE_ORDER, **key_dict
        )
        if not len(detail_list):
            return
        self.ori_detail = detail_list[0]
        self.lineEdit_paperno.setText(self.ori_detail['paperno'])
        self.lineEdit_client.setText(
            self.ori_detail['clientid'] + ' ' + self.ori_detail['clientname']
        )
        self.lineEdit_deliveryplace.setText(self.ori_detail['deliveryplace'])
        self.lineEdit_linkman.setText(self.ori_detail['linkman'])
        self.lineEdit_telno.setText(self.ori_detail['telno'])
        self.dateEdit_saledate.setDate(self.ori_detail['saledate'])
        self.dateEdit_deliverydate.setDate(self.ori_detail['deliverydate'])
        self.lineEdit_remark.setText(self.ori_detail['remark'])

    def set_paperno(self):
        res = self.SC.get_salenotes(True, *VALUES_TUPLE_PAPERNO)
        if not len(res):
            return ''
        max_paperno = res.order_by('-paperno')[0]
        num = re.findall('\d+', max_paperno)[-1]
        new_num = str(int(num) + 1)
        i = len(new_num)
        while i < len(num):
            new_num = '0' + new_num
            i += 1

        max_paperno = max_paperno.replace(num, new_num)
        self.lineEdit_paperno.setText(max_paperno)

    def set_conveyance_list(self):
        items = self.SC.get_salenotes(True, *VALUES_TUPLE_CONVEYANCE)\
            .distinct()
        if len(items):
            self.comboBox_conveyance.addItems(items)
        if len(self.ori_detail):
            self.comboBox_conveyance.setCurrentText(
                self.ori_detail['conveyance']
            )
        else:
            self.comboBox_conveyance.setCurrentText('')

    def set_paymethod_list(self):
        items = self.SC.get_salenotes(True, *VALUES_TUPLE_PAYMETHOD)\
            .distinct()
        if len(items):
            self.comboBox_paymethod.addItems(items)
        if len(self.ori_detail):
            self.comboBox_paymethod.setCurrentText(
                self.ori_detail['paymethod']
            )
        else:
            self.comboBox_paymethod.setCurrentText('')

    @pyqtSlot(str)
    def on_lineEdit_client_textChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        key_dict = {'clientid': id, 'clientname': name}
        res = self.SC.get_client(False, *VALUES_TUPLE_CLIENT, **key_dict)

        if len(res):
            client_detail = res[0]
            self.lineEdit_deliveryplace.setText(client_detail['address'])
            self.lineEdit_linkman.setText(client_detail['linkman'])
            self.lineEdit_telno.setText(client_detail['telno'])
            # self.new_detail['deliveryplace'] = client_detail['address']
            # self.new_detail['linkman'] = client_detail['linkman']
            # self.new_detail['telno'] = client_detail['telno']
            self.new_detail['salerid'] = client_detail['salerid']
            self.new_detail['salername'] = client_detail['salername']
        try:
            if id != self.ori_detail['clientid'] or name != self.ori_detail[
                'clientname']:
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

    @pyqtSlot(QDate)
    def on_dateEdit_saledate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['saledate']) is str:
                self.new_detail['saledate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['saledate']):
                self.new_detail['saledate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['saledate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['saledate'] = q_date.toPyDate()

    @pyqtSlot(QDate)
    def on_dateEdit_deliverydate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['deliverydate']) is str:
                self.new_detail['deliverydate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['bpdate']):
                self.new_detail['deliverydate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['bpdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['deliverydate'] = q_date.toPyDate()

    @pyqtSlot(str)
    def on_lineEdit_paperno_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['paperno']:
                self.new_detail['paperno'] = p_str
            else:
                try:
                    del self.new_detail['paperno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['paperno'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_deliveryplace_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['deliveryplace']:
                self.new_detail['deliveryplace'] = p_str
            else:
                try:
                    del self.new_detail['deliveryplace']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['deliveryplace'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_linkman_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['linkman']:
                self.new_detail['linkman'] = p_str
            else:
                try:
                    del self.new_detail['linkman']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['linkman'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_telno_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['telno']:
                self.new_detail['telno'] = p_str
            else:
                try:
                    del self.new_detail['telno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['telno'] = p_str

    @pyqtSlot(str)
    def on_comboBox_conveyance_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['conveyance']:
                self.new_detail['conveyance'] = p_str
            else:
                try:
                    del self.new_detail['conveyance']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['conveyance'] = p_str

    @pyqtSlot(str)
    def on_comboBox_paymethod_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['paymethod']:
                self.new_detail['paymethod'] = p_str
            else:
                try:
                    del self.new_detail['paymethod']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['paymethod'] = p_str

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
        if 'paperno' in self.new_detail:
            key_dict = {'paperno': self.new_detail['paperno']}
            res = self.SC.get_salenotes(True, *VALUES_TUPLE_PAPERNO, **key_dict)
            if len(res):
                msg = MessageBox(
                    self, text="单号重复，请修改后重新提交",
                    informative="已经存在单号为" + self.new_detail['paperno'] +
                                "的记录了！"
                )
                msg.show()
                self.lineEdit_paperno.setFocus()
                return
        self.new_detail['creatorid'] = user.user_id
        self.new_detail['creatorname'] = user.user_name
        self.SC.update_salenotes(self.autoid, **self.new_detail)
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLE_PAPERNO = ('paperno',)
VALUES_TUPLE_CONVEYANCE = ('conveyance',)
VALUES_TUPLE_PAYMETHOD = ('paymethod',)
VALUES_TUPLE_CLIENT = ('address', 'linkman', 'telno', 'salerid', 'salername')
VALUES_TUPLE_ORDER = (
    'autoid', 'paperno', 'clientid', 'clientname', 'saledate', 'deliverydate',
    'deliveryplace', 'conveyance', 'paymethod', 'remark', 'linkman', 'telno'
)
