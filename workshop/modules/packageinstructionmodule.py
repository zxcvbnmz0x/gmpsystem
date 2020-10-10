# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem

from PyQt5.QtCore import pyqtSlot, QDate

from stuff.controllers.stuffcontroller import StuffController
from product.controllers.productcontroller import ProductController

from workshop.views.packageinstruction import Ui_Form

import datetime

import user

class PackageInstructionModule(QWidget, Ui_Form):

    def __init__(self, autoid, parent=None):
        super(PackageInstructionModule, self).__init__(parent)
        self.autoid = autoid
        self.setupUi(self)
        self.SC = StuffController()
        self.PC = ProductController()
        self.ori_detail = dict()
        self.new_detail = dict()
        # 获取物料信息
        self.get_stufflist()
        # 获取批包装指令信息
        self.get_detail()

    # 获取已经领取了的物料
    def get_stufflist(self):
        values_tupe = (
            "autoid", "lrid", "stuffid", "stuffname", "batchno", "spec",
            "package", "presamount", "content", "cunit", "water",
            "impurity", "rdensity", "presunit"
        )
        key_dict = {
            'ppid': self.autoid,
            'stufftype__in': (3, 4)
        }
        res = self.SC.get_prodstuff(False, *values_tupe, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
                qtreeitem.setText(0, str(item['autoid']))  # autoid
                qtreeitem.setText(1, str(item['lrid']))  # lrid
                qtreeitem.setText(2, item['stuffid'] + ' ' + item[
                    'stuffname'])  # 物料
                qtreeitem.setText(3, item['batchno'])  # 进厂批号
                qtreeitem.setText(4, item['spec'])  # 含量规格
                qtreeitem.setText(5, item['package'])  # 包装规格
                qtreeitem.setText(6, str(item['presamount']) + item[
                    'presunit'])  # 计划量
                qtreeitem.setText(7, str(item['content']) + item[
                    'cunit'])  # 含量/效价
                qtreeitem.setText(8, str(item['water']) + '%')  # 水分
                qtreeitem.setText(9, str(item['impurity']))  # 相对密度
                qtreeitem.setText(10, str(item['rdensity']))  # 杂质

            self.treeWidget_stufflist.hideColumn(0)
            self.treeWidget_stufflist.hideColumn(1)
            for i in range(2, 11):
                self.treeWidget_stufflist.resizeColumnToContents(i)



    def get_detail(self):
        values_list = (
            'bpconstitutorid', 'bpconstitutorname', 'bpwarrantorid', 'bpwarrantorname',
            'bpexecutorid', 'bpexecutorname', 'bpconsdate', 'bpwarrantdate',
            'bpexecutedate', 'bpdate'
        )
        key_dict = {
            'autoid': self.autoid
        }
        res = self.PC.get_producingplan(False, *values_list, **key_dict)
        if len(res) == 0:
            return

        self.ori_detail = res[0]
        self.pushButton_bpconstitutor.setText(
            self.ori_detail['bpconstitutorid'] + ' ' +
            self.ori_detail['bpconstitutorname']
        )
        self.pushButton_bpwarrantor.setText(
            self.ori_detail['bpwarrantorid'] + ' ' +
            self.ori_detail['bpwarrantorname']
        )
        self.pushButton_bpexecutor.setText(
            self.ori_detail['bpexecutorid'] + ' ' +
            self.ori_detail['bpexecutorname']
        )
        if type(self.ori_detail['bpconsdate']) is datetime.date:
            self.dateEdit_bpconsdate.setDate(self.ori_detail['bpconsdate'])
        if type(self.ori_detail['bpwarrantdate']) is datetime.date:
            self.dateEdit_bpwarrantdate.setDate(self.ori_detail['bpwarrantdate'])
        if type(self.ori_detail['bpexecutedate']) is datetime.date:
            self.dateEdit_bpexecutedate.setDate(self.ori_detail['bpexecutedate'])
        else:
            self.dateEdit_bpexecutedate.setDate(user.now_date)
        if type(self.ori_detail['bpdate']) is datetime.date:
            self.dateEdit_bpdate.setDate(self.ori_detail['bpdate'])
        else:
            self.dateEdit_bpdate.setDate(user.now_date)

    @pyqtSlot(str)
    def on_pushButton_bpexecutor_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['bpexecutorid'] or name != self.ori_detail[
                'bpexecutorname']:
                self.new_detail['bpexecutorid'] = id
                self.new_detail['bpexecutorname'] = name
            else:
                try:
                    del self.new_detail['bpexecutorid']
                    del self.new_detail['bpexecutorname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['bpexecutorid'] = id
            self.new_detail['bpexecutorname'] = name

    @pyqtSlot(QDate)
    def on_dateEdit_bpexecutedate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['bpexecutedate']) is str:
                self.new_detail['bpexecutedate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['bpexecutedate']):
                self.new_detail['bpexecutedate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['bpexecutedate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['bpexecutedate'] = q_date.toPyDate()

    @pyqtSlot(QDate)
    def on_dateEdit_bpdate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['bpdate']) is str:
                self.new_detail['bpdate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['bpdate']):
                self.new_detail['bpdate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['bpdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['bpdate'] = q_date.toPyDate()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if len(self.new_detail):
            res = self.PC.update_producingplan(self.autoid, **self.new_detail)
            print(res)

