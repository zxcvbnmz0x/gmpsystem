# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from product.controllers.productcontroller import ProductController
from labrecord.controllers.labrecordscontroller import LabrecordsController
from workshop.controllers.workshopcontroller import WorkshopController
from stuff.controllers.stuffcontroller import StuffController

from workshop.views.preprodputinnote import Ui_Form

from lib.utils.messagebox import MessageBox
from lib.utils.util import to_str

import datetime
import decimal

import user


class PreProdPutInModule(QWidget, Ui_Form):
    accepted = pyqtSignal()

    def __init__(self, autoid:int=0, ppid: int=0, parent=None):
        super(PreProdPutInModule, self).__init__(parent)
        self.setupUi(self)
        self.ppid = ppid
        self.autoid = autoid
        self.content = decimal.Decimal('-1')
        self.water = decimal.Decimal('-1')
        self.rdensity = decimal.Decimal('-1')
        self.impurity = decimal.Decimal('-1')
        self.lrid = 0
        self.checkdate = user.now_date
        # self.units = set()
        self.unit = ''
        self.cunit = '%'
        self.expireddays = 730
        self.countercheckdays = 365
        self.WC = WorkshopController()
        self.LC = LabrecordsController()
        self.PC = ProductController()
        self.SC = StuffController()
        self.product_detail = dict()
        self.ori_detail = dict()
        self.new_detail = dict()

        # 把autoid和ppid补全
        self.get_autoid_or_ppid()
        # 获取入库位置的下拉选项
        self.get_postiton()

        # 整箱数量的校验器
        self.set_valitor(self.lineEdit_amount, 0)
        # 获取产品信息
        self.get_productdetail()
        # 设置含量单位、复检日期、有效期等参数
        self.basicdetail()

        # 获取报告书的状态和编号
        self.get_labdetail()
        # 获取入库信息
        self.get_putinnote()

    def get_autoid_or_ppid(self):
        values_list = ('autoid', 'ppid')
        if self.autoid:
            key_dict = {'autoid': self.autoid}
        else:
            key_dict = {'ppid': self.ppid}
        res = self.WC.get_productputinnote(False, *values_list, **key_dict)
        if not len(res):
            return
        if self.autoid:
            self.ppidid = res[0]['ppid']
        else:
            self.autoid = res[0]['autoid']

    def set_valitor(self, widget, bottom=0, top=0):
        intvalitor = QIntValidator()
        intvalitor.setBottom(bottom)
        if top != 0:
            intvalitor.setTop(top)
        widget.setValidator(intvalitor)

    def get_postiton(self):

        key_dict_ws = {
            'ppid': self.ppid
        }
        ws_list = self.WC.get_productputinnote(
            True, *VALUES_LIST_WS, **key_dict_ws
        )
        if not len(ws_list):
            return
        warehouseid = ws_list[0]

        values_list_positon = ('position',)
        key_dict_position = {
            'warehouseid': warehouseid
        }
        pos_list = self.WC.get_productputinnote(
            True, *values_list_positon, **key_dict_position)
        if len(pos_list):
            self.comboBox_piposition.addItems(pos_list.distinct())

    def get_productdetail(self):

        key_dict = {
            'autoid': self.ppid
        }
        res = self.PC.get_producingplan(
            False, *VALUES_LIST_PROD, **key_dict
        )
        if len(res) != 1:
            return
        self.product_detail = res[0]
        self.label_product.setText(
            self.product_detail['prodid'] + ' ' + \
            self.product_detail['prodname']
        )
        self.label_spec.setText(self.product_detail['spec'])
        self.label_package.setText(self.product_detail['package'])
        self.label_unit.setText(self.product_detail['basicunit'])

    def basicdetail(self):
        stuffid = self.product_detail['prodid']
        stuffname = self.product_detail['prodname']
        key_dict = {
            'stuffid': stuffid,
            'stuffname': stuffname
        }
        res = self.SC.get_stuffdict(False, *VALUES_TUPLE_STUFF, **key_dict)
        if not len(res):
            return
        self.cunit = res[0]['cunit']
        self.expireddays = res[0]['expireddays']
        self.countercheckdays = res[0]['countercheckdays']
        self.label_contentunit.setText(self.cunit)

    def get_labdetail(self):
        values_list = ('autoid', 'paperno', 'status', 'reportdate')
        key_dict = {
            'labtype': 2,
            'ciid': self.ppid
        }
        res = self.LC.get_labrecord(
            False, *values_list, **key_dict
        )
        if not len(res):
            return
        # 选择最后一条符合条件的成品报告
        detail = res.order_by('-autoid')[0]
        self.lrid = detail['autoid']
        self.checkdate = detail['reportdate']
        self.label_reportpaperno.setText(detail['paperno'])
        self.label_checkstatus.setText(CHECK_STATUS[detail['status']])

    def get_putinnote(self):

        key_dict = {
            'autoid': self.autoid
        }
        res = self.WC.get_productputinnote(
            False, *VALUES_TUPLE_PUTIN, **key_dict
        )
        if not len(res):
            return
        # 选择第一条
        self.ori_detail = res[0]

        self.label_warehouse.setText(
            self.ori_detail['warehouseid'] + ' ' +
            self.ori_detail['warehousename']
        )
        self.comboBox_piposition.setCurrentText(self.ori_detail['position'])
        self.pushButton_applyer.setText(
            self.ori_detail['piapplyerid'] + ' ' +
            self.ori_detail['piapplyername']
        )
        self.pushButton_qa.setSign(
            self.ori_detail['piqaid'] + ' ' + self.ori_detail['piqaname']
        )
        self.pushButton_piwsman.setSign(
            self.ori_detail['warehousemanid'] + ' ' +
            self.ori_detail['warehousemanname']
        )
        self.lineEdit_amount.setText(to_str(self.ori_detail['piamount']))


        if self.ori_detail['pistatus'] == 0:
            self.pushButton_accept.setVisible(True)
            self.pushButton_save.setVisible(True)
            self.pushButton_cancel.setVisible(False)
            self.pushButton_pi.setVisible(False)
        elif self.ori_detail['pistatus'] == 1:
            self.pushButton_accept.setVisible(False)
            self.pushButton_save.setVisible(False)
            self.pushButton_cancel.setVisible(True)
            self.pushButton_pi.setVisible(True)
        elif self.ori_detail['pistatus'] == 3:
            self.pushButton_accept.setVisible(False)
            self.pushButton_save.setVisible(False)
            self.pushButton_cancel.setVisible(False)
            self.pushButton_pi.setVisible(False)

    @pyqtSlot(str)
    def on_lineEdit_amount_textEdited(self, p_str):
        if p_str == '':
            amount = decimal.Decimal('0')
        else:
            amount = decimal.Decimal(p_str)
        try:
            if amount != self.ori_detail['piamount']:
                self.new_detail['piamount'] = amount
            else:
                try:
                    del self.new_detail['piamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['piamount'] = amount

    @pyqtSlot(str)
    def on_pushButton_qa_signChanged(self, p_str):
        if p_str not in  ('', ' '):
            self.pushButton_accept.setEnabled(True)
            piqaid, piqaname = p_str.split(' ')
        else:
            self.pushButton_accept.setEnabled(False)
            piqaid, piqaname = ('', '')
        try:
            if piqaid != self.ori_detail['piqaid']:
                self.new_detail['piqaid'] = piqaid
                self.new_detail['piqaname'] = piqaname
            else:
                try:
                    del self.new_detail['piqaid']
                    del self.new_detail['piqaname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['piqaid'] = piqaid
            self.new_detail['piqaname'] = piqaname

    @pyqtSlot(str)
    def on_pushButton_applyer_signChanged(self, p_str):
        if p_str not in ('', ' '):
            piapplyerid, piapplyername = p_str.split(' ')
        else:
            piapplyerid, piapplyername = ('', '')
        try:
            if piapplyerid != self.ori_detail['piapplyerid']:
                self.new_detail['piapplyerid'] = piapplyerid
                self.new_detail['piapplyername'] = piapplyername
            else:
                try:
                    del self.new_detail['piapplyerid']
                    del self.new_detail['piapplyername']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['piapplyerid'] = piapplyerid
            self.new_detail['piapplyername'] = piapplyername

    @pyqtSlot(str)
    def on_comboBox_piposition_currentTextChanged(self, p_str):
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
    def on_pushButton_save_clicked(self):
        if self.has_changed():
            self.WC.update_productputinnote(self.autoid, **self.new_detail)

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if self.lineEdit_amount.text() in ('', '0'):
            msg = MessageBox(self, text="入库数量不能未空")
            msg.show()
            return
        if self.pushButton_applyer.text() in ('', ' '):
            self.pushButton_applyer.setSign(user.user_id + ' ' +user.user_name)
            self.new_detail['piapplyerid'] = user.user_id
            self.new_detail['piapplyername'] = user.user_name
            self.new_detail['pidate'] = user.now_date
        self.new_detail['pistatus'] = 1

        self.WC.update_productputinnote(self.autoid, **self.new_detail)
        realamount = decimal.Decimal(self.lineEdit_amount.text())
        detail = {'realamount': realamount}
        self.PC.update_producingplan(self.ppid, **detail)

        self.pushButton_save.setVisible(False)
        self.pushButton_accept.setVisible(False)
        self.pushButton_cancel.setVisible(True)
        self.pushButton_pi.setVisible(True)
        self.accepted.emit()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.new_detail['piapplyerid'] = ''
        self.new_detail['piapplyername'] = ''
        self.new_detail['pistatus'] = 0

        self.WC.update_productputinnote(self.autoid, **self.new_detail)

        self.pushButton_save.setVisible(True)
        self.pushButton_accept.setVisible(True)
        self.pushButton_cancel.setVisible(False)
        self.pushButton_pi.setVisible(False)
        self.accepted.emit()

    @pyqtSlot()
    def on_pushButton_pi_clicked(self):
        if self.label_checkstatus.text() != '检验合格':
            mesgbox = MessageBox(
                parent=self, title="提示", text="当前产品尚未检验合格无法入库"
            )
            mesgbox.exec()
            return

        self.new_detail['warehousemanid'] = user.user_id
        self.new_detail['warehousemanname'] = user.user_name
        self.new_detail['pidate'] = user.now_date
        self.new_detail['pistatus'] = 3

        # 计算要入库的产品信息
        putin_msg = self.get_putin_msg()
        res = self.WC.update_preproductputinnote(
            self.autoid, putin_msg, **self.new_detail
        )
        if not res:
            return
        self.pushButton_piwsman.setSign(user.user_id + ' ' + user.user_name)
        self.pushButton_save.setVisible(False)
        self.pushButton_accept.setVisible(False)
        self.pushButton_cancel.setVisible(False)
        self.pushButton_pi.setVisible(False)
        self.accepted.emit()

    def get_putin_msg(self):

        return_dict = self.product_detail
        return_dict['stuffid'] = return_dict.pop('prodid')
        return_dict['stuffname'] = return_dict.pop('prodname')
        return_dict['stuffkind'] = return_dict.pop('commonname')
        return_dict['ciid'] = self.autoid
        return_dict['pltype'] = 1
        return_dict['stufftype'] = 1
        return_dict['expireddate'] = self.product_detail['makedate'] + \
            datetime.timedelta(days=self.expireddays)
        return_dict['amount'] = decimal.Decimal(self.lineEdit_amount.text())
        return_dict['piamount'] = decimal.Decimal(self.lineEdit_amount.text())
        return_dict['position'] = self.comboBox_piposition.currentText()
        return_dict['checkindate'] = user.now_date
        return_dict['putindate'] = user.now_date
        return_dict['warehousemanid'] = user.user_id
        return_dict['warehousemanname'] = user.user_name
        return_dict['content'] = self.content
        return_dict['cunit'] = self.cunit
        return_dict['water'] = self.water
        return_dict['rdensity'] = self.rdensity
        return_dict['impurity'] = self.impurity
        return_dict['lrid'] = self.lrid
        return_dict['checkdate'] = self.checkdate
        return_dict['nextcheckdate'] = self.checkdate + \
            datetime.timedelta(days=self.countercheckdays)
        return_dict['deptid'] = self.ori_detail['warehouseid']
        return_dict['deptname'] = self.ori_detail['warehousename']
        return return_dict


    def has_changed(self):
        if not len(self.new_detail):
            return False
        if self.pushButton_applyer.text() in ('', ' '):
            self.pushButton_applyer.setSign(user.user_id + ' ' +user.user_name)
            self.new_detail['piapplyerid'] = user.user_id
            self.new_detail['piapplyername'] = user.user_name
        return True

CHECK_STATUS = ("待请验", "待取样", "检验中", "检验合格", "检验不合格")
VALUES_LIST_PROD = (
    'prodid', 'prodname', 'spec', 'package', 'basicunit', 'commonname',
    'bpunit', 'mpunit', 'spunit', 'spamount', 'mpamount', 'basicunit',
    'allowno', 'batchno', 'makedate', 'basicamount'
)

VALUES_LIST_WS = ("warehouseid",)
VALUES_TUPLE_STUFF = {'cunit', 'expireddays', 'countercheckdays'}

VALUES_TUPLE_PUTIN = (
            "pidate", "piapplyerid", "piapplyername", "piqaid", "piqaname",
            "warehousemanid", "warehousemanname", "pistatus", "position",
            "warehouseid", "warehousename", "piamount"
        )