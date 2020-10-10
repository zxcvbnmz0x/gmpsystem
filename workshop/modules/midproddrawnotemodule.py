# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QTreeWidgetItemIterator

from PyQt5.QtCore import pyqtSlot, QDate

from product.controllers.productcontroller import ProductController

from workshop.views.midproddrawnote import Ui_Form

import datetime

import user

class MidproddrawnoteModule(QWidget, Ui_Form):
    """ 半成品登记/发放记录
    autoid: 登记/发放表的ppid
    kind: 0为登记记录，1为发放记录
    """

    def __init__(self, autoid, kind, parent=None):
        super(MidproddrawnoteModule, self).__init__(parent)
        self.autoid = autoid
        self.kind = kind
        self.setupUi(self)
        self.PC = ProductController()
        self.ori_detail = dict()
        self.new_detail = dict()

        if kind == 0:
            self.treeWidget_midproductlist.headerItem().setText(3, "中间站登记人")
            self.treeWidget_midproductlist.headerItem().setText(5, "登记工人")
        elif kind == 1:
            self.treeWidget_midproductlist.headerItem().setText(3, "中间站发放人")
            self.treeWidget_midproductlist.headerItem().setText(5, "领料工人")
        # 获取半成品信息
        self.get_midprod()
        # 获取半成品的登记/发放状态
        self.get_midstatus()

    def get_midprod(self):
        self.treeWidget_midproductlist.clear()
        values_list = ["autoid", "container", "amount", "unit"]
        if self.kind == 0:
            reg_list = [
                "registrarid", "registrarname", "regtime", "workerid",
                "workername"
            ]
        elif self.kind == 1:
            reg_list = [
                "providerid", "providername", "drawtime", "drawerid",
                "drawername"
            ]
        values_list += reg_list
        key_dict = {
            'ppid': self.autoid
        }
        res = self.PC.get_midproddrawnotes(True, *values_list, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_midproductlist)
                qtreeitem.setText(0, str(item[0]))  # autoid
                qtreeitem.setText(1, str(item[1]))  # 桶号
                qtreeitem.setText(2, str(item[2]) + item[3])  # 数量
                qtreeitem.setText(3, item[4] + ' ' + item[5])  # 登记人/发放人
                qtreeitem.setText(4, str(item[6]))  # 登记/发放日期
                qtreeitem.setText(5, item[7] + ' ' + item[8])  # 工人

            self.treeWidget_midproductlist.hideColumn(0)
            for i in range(1, 6):
                self.treeWidget_midproductlist.resizeColumnToContents(i)

    def get_midstatus(self):
        values_tuple = ("midstatus",)
        key_dict = {
            'autoid': self.autoid
        }
        res = self.PC.get_producingplan(False, *values_tuple, **key_dict)
        if len(res) == 1:
            if res[0]['midstatus'] > 2 and self.kind == 0:
                # 已经完成发放记录，则无法修改登记记录
                self.pushButton_workersign.setVisible(False)
            elif res[0]['midstatus'] == 0 and self.kind == 1:
                # 还没有完成登记，则无法修改发放记录
                self.pushButton_workersign.setVisible(False)

    @pyqtSlot()
    def on_pushButton_workersign_clicked(self):
        it = QTreeWidgetItemIterator(self.treeWidget_midproductlist)

        id_list = []
        while it.value():
            item = it.value()
            id_list.append(int(item.text(0)))
            it += 1
        if not len(id_list):
            return
        detail = dict()
        status : int
        if self.kind == 0:
            detail = {
                'workerid': user.user_id,
                'workername': user.user_name
            }
            status = 1
        elif self.kind == 1:
            detail = {
                'drawerid': user.user_id,
                'drawername': user.user_name
            }
            status = 2

        res = self.PC.update_midproddrawnotes(id_list, self.autoid, status, **detail)
        if res > 0:
            self.get_midprod()

