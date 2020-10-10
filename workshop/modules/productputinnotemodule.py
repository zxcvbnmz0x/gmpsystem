# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem
from PyQt5.QtGui import QIntValidator
from PyQt5.QtCore import pyqtSignal, pyqtSlot

from product.controllers.productcontroller import ProductController
from labrecord.controllers.labrecordscontroller import LabrecordsController
from workshop.controllers.workshopcontroller import WorkshopController

from workshop.views.productputinnote import Ui_Form

from lib.utils.messagebox import MessageBox

import datetime
import decimal

import user


class ProductputinModule(QWidget, Ui_Form):
    accepted = pyqtSignal()

    def __init__(self, autoid:int=0, ppid: int=0, parent=None):
        super(ProductputinModule, self).__init__(parent)
        self.setupUi(self)
        self.ppid = ppid

        self.autoid = autoid
        self.bpamount = decimal.Decimal('0')
        self.mpamount = decimal.Decimal('0')
        self.spamount = decimal.Decimal('0')
        self.a_box_samount = decimal.Decimal('0')
        self.oddments_list = []
        self.units = set()
        self.WC = WorkshopController()
        self.LC = LabrecordsController()
        self.PC = ProductController()
        self.product_detail = dict()
        self.ori_detail = dict()
        self.new_detail = dict()

        if not self.ppid and not self.autoid:
            return
        # 把autoid和ppid补全
        self.get_autoid_or_ppid()
        # 获取产品信息
        self.get_productdetail()
        # 设置比例、一箱数量等参数
        self.basicdetail()
        # 获取寄库和入库位置的下拉选项
        self.get_postiton()
        # 获取报告书的状态和编号
        self.get_labdetail()
        # 获取入库信息
        self.get_putinnote()
        # 获取零头领取信息
        self.get_oddment()
        # 整箱数量的校验器
        self.set_valitor(self.lineEdit_amount, 0)
        # 零头数量的校验器
        self.set_valitor(self.lineEdit_oddment, 0, self.a_box_samount)

    def get_autoid_or_ppid(self):
        values_list = ('autoid', 'ppid')
        if self.autoid:
            key_dict = {'autoid': self.autoid}
        else:
            key_dict = {'ppid': self.ppid}
        res = self.WC.get_productputinnote(False, *values_list, **key_dict)
        if not len(res):
            return
        self.autoid = res[0]['autoid']
        self.ppidid = res[0]['ppid']

    def set_valitor(self, widget, bottom=0, top=0):
        intvalitor = QIntValidator()
        intvalitor.setBottom(bottom)
        if top != 0:
            intvalitor.setTop(top)
        widget.setValidator(intvalitor)

    def get_postiton(self):
        values_list_ws = ("warehouseid",)
        key_dict_ws = {
            'ppid': self.ppid
        }
        ws_list = self.WC.get_productputinnote(
            True, *values_list_ws, **key_dict_ws
        )
        if not len(ws_list):
            return
        warehouseid = ws_list[0]

        values_list_dppositon = ('dpposition',)
        values_list_positon = ('position',)
        key_dict_position = {
            'warehouseid': warehouseid
        }
        dppos_list = self.WC.get_productputinnote(
            True, *values_list_dppositon, **key_dict_position)
        pos_list = self.WC.get_productputinnote(
            True, *values_list_positon, **key_dict_position)
        if len(dppos_list):
            self.comboBox_dpposition.addItems(dppos_list.distinct())
        if len(pos_list):
            self.comboBox_piposition.addItems(pos_list.distinct())

    def get_productdetail(self):
        values_list = (
            "prodid", "prodname", "spec", "package", "bpamount", "bpunit",
            "mpamount", "mpunit", "spamount", "spunit"
        )
        key_dict = {
            'autoid': self.ppid
        }
        res = self.PC.get_producingplan(
            False, *values_list, **key_dict
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
        self.label_piunit.setText(self.product_detail['spunit'])
        self.label_dpunit.setText(self.product_detail['spunit'])

    def basicdetail(self):
        if self.product_detail['bpamount'] != decimal.Decimal('0'):
            self.bpamount = self.product_detail['bpamount']
        else:
            self.bpamount = decimal.Decimal('1')
        if self.product_detail['mpamount'] != decimal.Decimal('0'):
            self.mpamount = self.product_detail['mpamount']
        else:
            self.mpamount = decimal.Decimal('1')
        if self.product_detail['spamount'] != decimal.Decimal('0'):
            self.spamount = self.product_detail['spamount']
        else:
            self.spamount = decimal.Decimal('1')
        self.a_box_samount = self.bpamount * self.mpamount * self.spamount
        self.units = [
            self.product_detail['bpunit'], self.product_detail['mpunit'],
            self.product_detail['spunit']
        ]

    def get_labdetail(self):
        values_list = ("paperno", "status")
        key_dict = {
            'labtype': 3,
            'ciid': self.ppid
        }
        res = self.LC.get_labrecord(
            False, *values_list, **key_dict
        )
        if not len(res):
            return
        # 选择最后一条符合条件的成品报告
        detail = res.order_by('-autoid')[0]
        self.label_reportpaperno.setText(detail['paperno'])
        self.label_checkstatus.setText(CHECK_STATUS[detail['status']])

    def get_putinnote(self):
        values_list = (
            "dpamount", "piamount", "packamount", "unittype",
            "pidate", "piapplyerid", "piapplyername", "piqaid", "piqaname",
            "warehousemanid", "warehousemanname", "pistatus", "position",
            "dpposition", "dpwarehousemanid", "dpwarehousemanname",
            "warehouseid", "warehousename", "oddment", "dpdate", "oddment"
        )
        key_dict = {
            'autoid': self.autoid
        }
        res = self.WC.get_productputinnote(
            False, *values_list, **key_dict
        )
        if not len(res):
            return
        # 选择第一条
        self.ori_detail = res[0]

        self.label_dpdate.setText(
            str(self.ori_detail['dpdate']) if type(self.ori_detail['dpdate'])
                                              is datetime.date else ''
        )
        self.label_pidate.setText(
            str(self.ori_detail['pidate']) if type(self.ori_detail['pidate'])
                                              is datetime.date else ''
        )
        self.comboBox_unittype.setCurrentIndex(self.ori_detail['unittype'])
        self.label_warehouse.setText(
            self.ori_detail['warehouseid'] + ' ' +
            self.ori_detail['warehousename']
        )
        self.comboBox_dpposition.setCurrentText(self.ori_detail['dpposition'])
        self.comboBox_piposition.setCurrentText(self.ori_detail['position'])
        self.pushButton_applyer.setText(
            self.ori_detail['piapplyerid'] + ' ' +
            self.ori_detail['piapplyername']
        )
        self.pushButton_qa.setSign(
            self.ori_detail['piqaid'] + ' ' + self.ori_detail['piqaname']
        )
        self.pushButton_dpwsman.setText(
            self.ori_detail['dpwarehousemanid'] + ' ' +
            self.ori_detail['dpwarehousemanname']
        )
        self.pushButton_piwsman.setText(
            self.ori_detail['warehousemanid'] + ' ' +
            self.ori_detail['warehousemanname']
        )

        self.lineEdit_amount.setText(str(self.ori_detail['dpamount']))
        self.lineEdit_oddment.setText(str(self.ori_detail['oddment']))
        self.label_unit.setText(self.units[self.ori_detail['unittype']])
        self.label_oddmentunit.setText(self.units[2])

        self.label_dpamount.setText(str(self.ori_detail['piamount']))
        self.label_piamount.setText(str(self.ori_detail['piamount']))

        if self.ori_detail['pistatus'] == 0:
            self.pushButton_accept.setVisible(True)
            self.pushButton_save.setVisible(True)
            self.pushButton_cancel.setVisible(False)
            self.pushButton_dp.setVisible(False)
            self.pushButton_pi.setVisible(False)
        elif self.ori_detail['pistatus'] == 1:
            self.pushButton_accept.setVisible(False)
            self.pushButton_save.setVisible(False)
            self.pushButton_cancel.setVisible(True)
            self.pushButton_dp.setVisible(True)
            self.pushButton_pi.setVisible(False)
        elif self.ori_detail['pistatus'] == 2:
            self.pushButton_accept.setVisible(False)
            self.pushButton_save.setVisible(False)
            self.pushButton_cancel.setVisible(False)
            self.pushButton_dp.setVisible(False)
            self.pushButton_pi.setVisible(True)
        elif self.ori_detail['pistatus'] == 3:
            self.pushButton_accept.setVisible(False)
            self.pushButton_save.setVisible(False)
            self.pushButton_cancel.setVisible(False)
            self.pushButton_dp.setVisible(False)
            self.pushButton_pi.setVisible(False)

    def get_oddment(self):
        self.treeWidget_oddments.clear()
        self.treeWidget_oddments.hideColumn(0)
        values_list = ("autoid", "batchno", "amount", "unit", "makedate")
        key_dict = {
            'dppid': self.ppid
        }
        res = self.PC.get_oddmentdrawnotes(False, *values_list, **key_dict)
        if not len(res):
            return

        for item in res:
            if item['unit'] not in self.units:
                continue
            qtreeitem = QTreeWidgetItem(self.treeWidget_oddments)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['batchno'])
            qtreeitem.setText(2, str(item['amount']))
            qtreeitem.setText(3, item['unit'])
            qtreeitem.setText(4, str(self.a_box_samount - item['amount']))
            qtreeitem.setText(5, str(item['makedate']))
            self.oddments_list.append(
                (2, self.ppid, self.a_box_samount - item['amount'],
                 item['autoid'], item['amount'])
            )
        for i in range(1, 6):
            self.treeWidget_oddments.resizeColumnToContents(i)
        if self.treeWidget_oddments.topLevelItemCount() > 0:
            self.checkBox_has_draw_oddments.setCheckState(2)

    @pyqtSlot(int)
    def on_comboBox_unittype_currentIndexChanged(self, p_int):
        self.label_unit.setText(self.units[p_int])
        try:
            if p_int != self.ori_detail['unittype']:
                self.new_detail['unittype'] = p_int
            else:
                try:
                    del self.new_detail['unittype']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['unittype'] = p_int

    @pyqtSlot(str)
    def on_lineEdit_amount_textEdited(self, p_str):
        if p_str == '':
            amount = decimal.Decimal('0')
        else:
            amount = decimal.Decimal(p_str)
        try:
            if amount != self.ori_detail['dpamount']:
                self.new_detail['dpamount'] = amount
            else:
                try:
                    del self.new_detail['dpamount']
                except KeyError:
                    pass

            self.set_total_amount()

        except KeyError:
            self.new_detail['dpamount'] = amount
        except decimal.InvalidOperation:
            pass

    def set_total_amount(self):
        amount = decimal.Decimal(self.lineEdit_amount.text())
        oddment = decimal.Decimal(self.lineEdit_oddment.text())
        unit_index = self.comboBox_unittype.currentIndex()
        this_batchno_amount = 0
        if unit_index == 0:
            this_batchno_amount = amount * self.a_box_samount + oddment
        elif unit_index == 1:
            this_batchno_amount = amount * self.mpamount * self.spamount + oddment
        elif unit_index == 2:
            this_batchno_amount = amount * self.spamount + oddment
        merge_amount = self.treeWidget_oddments.topLevelItemCount() * \
                       self.a_box_samount
        piamount = this_batchno_amount + merge_amount
        self.label_dpamount.setText(str(piamount))
        self.label_piamount.setText(str(piamount))
        try:
            if piamount != self.ori_detail['piamount']:
                self.new_detail['piamount'] = piamount
            else:
                try:
                    del self.new_detail['piamount']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['piamount'] = piamount

    @pyqtSlot(str)
    def on_lineEdit_oddment_textEdited(self, p_str):
        if p_str == '':
            amount = decimal.Decimal('0')
        else:
            amount = decimal.Decimal(p_str)
        try:
            if amount != self.ori_detail['oddment']:
                self.new_detail['oddment'] = amount
            else:
                try:
                    del self.new_detail['oddment']
                except KeyError:
                    pass
            self.set_total_amount()
        except KeyError:
            self.new_detail['oddment'] = amount
        except decimal.InvalidOperation:
            pass

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
    def on_comboBox_dpposition_currentTextChanged(self, p_str):
        try:
            if p_str != self.ori_detail['dpposition']:
                self.new_detail['dpposition'] = p_str
            else:
                try:
                    del self.new_detail['dpposition']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['dpposition'] = p_str

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
        if self.pushButton_applyer.text() in ('', ' '):
            self.pushButton_applyer.setSign(user.user_id + ' ' +user.user_name)
            self.new_detail['piapplyerid'] = user.user_id
            self.new_detail['piapplyername'] = user.user_name
            self.new_detail['dpdate'] = user.now_date
        self.new_detail['pistatus'] = 1

        self.WC.update_productputinnote(self.autoid, **self.new_detail)
        realamount = decimal.Decimal(self.label_piamount.text())
        detail = {'realamount': realamount}
        self.PC.update_producingplan(self.ppid, **detail)

        self.pushButton_save.setVisible(False)
        self.pushButton_accept.setVisible(False)
        self.pushButton_cancel.setVisible(True)
        self.pushButton_dp.setVisible(False)
        self.pushButton_pi.setVisible(False)
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
        self.pushButton_dp.setVisible(False)
        self.pushButton_pi.setVisible(False)
        self.accepted.emit()

    @pyqtSlot()
    def on_pushButton_dp_clicked(self):
        self.new_detail['dpwarehousemanid'] = user.user_id
        self.new_detail['dpwarehousemanname'] = user.user_name
        self.new_detail['pistatus'] = 2

        self.WC.update_productputinnote(self.autoid, **self.new_detail)

        self.pushButton_save.setVisible(False)
        self.pushButton_accept.setVisible(False)
        self.pushButton_cancel.setVisible(False)
        self.pushButton_dp.setVisible(False)
        self.pushButton_pi.setVisible(True)
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
        self.WC.update_productputinnote(self.autoid, True, putin_msg, **self.new_detail)

        self.pushButton_save.setVisible(False)
        self.pushButton_accept.setVisible(False)
        self.pushButton_cancel.setVisible(False)
        self.pushButton_dp.setVisible(False)
        self.pushButton_pi.setVisible(False)
        self.accepted.emit()

    def get_putin_msg(self):
        return_detail = []
        return_detail += self.oddments_list
        # 全部的入库数量
        all_amount = decimal.Decimal(self.label_piamount.text())
        # 本批零头数量
        oddment_amount = decimal.Decimal(self.lineEdit_oddment.text())
        return_detail.append((1, self.ppid, oddment_amount, 0, 0))
        # 合箱数量
        merge_amount = decimal.Decimal(self.treeWidget_oddments.topLevelItemCount()) * self.a_box_samount

        # 本批整箱数量
        spamount_of_total_box = all_amount - oddment_amount - merge_amount
        return_detail.append((0, self.ppid, spamount_of_total_box,0 ,0))
        return return_detail

    def has_changed(self):
        if not len(self.new_detail):
            return False
        if self.pushButton_applyer.text() in ('', ' '):
            self.pushButton_applyer.setSign(user.user_id + ' ' +user.user_name)
            self.new_detail['piapplyerid'] = user.user_id
            self.new_detail['piapplyername'] = user.user_name
        return True

CHECK_STATUS = ("待请验", "待取样", "检验中", "检验合格", "检验不合格")
