# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem
from PyQt5.QtCore import pyqtSlot
from warehouse.views.newpurchaseregistration import Ui_Dialog

from warehouse.controllers.warehousecontroller import WarehouseController
from supplyer.controllers.supplyercontroller import SupplyerController

import re

import user


class NewPurchRegModule(QDialog, Ui_Dialog):
    
    def __init__(self, parent=None):
        super(NewPurchRegModule, self).__init__(parent)
        self.order_list = []
        self.detail = dict()
        self.paperno = ''
        self.setupUi(self)
        self.WC = WarehouseController()
        self.SC = SupplyerController()

        self.get_orderlist()

    def get_orderlist(self):
        self.treeWidget_orderlist.clear()
        # self.treeWidget_orderlist.hideColumn(0)
        key_dict = {'status': 1}
        self.order_list = self.SC.get_purchasingplan(
            False, *VALUES_TUPLE_ORDER, **key_dict
        )
        if not len(self.order_list):
            return
        for item in self.order_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_orderlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['paperno'])
            qtreeitem.setText(2, str(item['createdate']))
            qtreeitem.setText(3, item['supid'] + ' ' + item['supname'])
            qtreeitem.setText(4, item['creatorid'] + ' ' + item['creatorname'])
        for i in range(2, 5):
            self.treeWidget_orderlist.resizeColumnToContents(i)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemDoubleClicked(self, qtreeitem, p_int):
        id = int(qtreeitem.text(0))
        for item in self.order_list:
            if id == item['autoid']:
                self.detail = item
                break
        if len(self.detail):
            self.paperno = self.set_regpaperno()
            self.lineEdit_regno.setText(self.paperno)
            self.lineEdit_purchdate.setText(str(self.detail['createdate']))
            self.lineEdit_buyer.setText(
                str(self.detail['creatorid']) + ' ' + self.detail['creatorname']
            )
            self.lineEdit_remark.setText(str(self.detail['remark']))
            self.lineEdit_supplyer.setText(str(
                self.detail['supid'] + ' ' + self.detail['supname'])
            )
            self.lineEdit_purchno.setText(self.detail['paperno'])

    def set_regpaperno(self):
        key_dict = {'papertype': 0}
        res = self.WC.get_stuffcheckin(True, *VALUES_TUPLE_PAPERNO, **key_dict)
        if not len(res):
            return '0001'
        max_paperno = res.order_by('-paperno')[0]
        num = re.findall('\d+', max_paperno)[-1]
        new_num = str(int(num) + 1)
        i = len(new_num)
        while i < len(num):
            new_num = '0' + new_num
            i += 1

        return max_paperno.replace(num, new_num)

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if not self.detail:
            return
        kwargs = {
            'paperno': self.paperno,
            'pppaperno': self.detail['paperno'],
            'createdate': user.now_date,
            'creatorid': user.user_id,
            'creatorname': user.user_name,
            'supid': self.detail['supid'],
            'supname': self.detail['supname'],
            'remark': self.detail['remark'],
            'buyerid': self.detail['creatorid'],
            'buyername': self.detail['creatorname'],
            'buydate': self.detail['invaliddate'],
            'pikind': '采购',
            'papertype': 0,
            'status':0
        }
        self.WC.new_stuffcheckin(self.detail['autoid'], **kwargs)
        self.accept()


    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

VALUES_TUPLE_PAPERNO = ('paperno',)

VALUES_TUPLE_ORDER = (
    'autoid', 'paperno', 'createdate', 'supid', 'supname', 'creatorid',
    'creatorname', 'remark', 'invaliddate'
)
