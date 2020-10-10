# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QTreeWidgetItem, QDialog, QTreeWidgetItemIterator

from PyQt5.QtCore import pyqtSlot

from product.controllers.productcontroller import ProductController

from workshop.views.selectoddmentdraw import Ui_Dialog

import user


class SelectoddmentdrawModule(QDialog, Ui_Dialog):

    def __init__(self, ppid, parent=None):
        super(SelectoddmentdrawModule, self).__init__(parent)
        self.setupUi(self)
        self.ppid = ppid
        self.prodid = ''
        self.id_list = tuple()
        self.PC = ProductController()
        # 获取ppid对应的prodid
        self.get_prodid()
        # 查找prodid相同的记录，并保存这些记录的id_list
        self.get_id_list()
        # 零头记录中找到没有过有效期且没有被领取（dppid=0）
        self.get_oddments_list()

    def get_prodid(self):
        values_list = ('prodid',)
        key_dict = {
            'autoid': self.ppid
        }
        res = self.PC.get_producingplan(True, *values_list, **key_dict)
        if len(res) == 1:
            self.prodid = res[0]

    def get_id_list(self):
        if not self.prodid:
            return
        values_list = ('autoid', )
        key_dict = {
            'prodid': self.prodid
        }
        res = self.PC.get_producingplan(True, *values_list, **key_dict)
        # 去除本批ppid
        self.id_list = list(res)
        self.id_list .remove(self.ppid)

    def get_oddments_list(self):
        self.treeWidget_oddmentdrawlist.clear()
        self.treeWidget_oddmentdrawlist.hideColumn(0)

        values_list = (
            'autoid', 'batchno', 'amount', 'unit', 'registerid', 'registername',
            'regdate', 'invaliddate'
        )
        # 没有发放，没有寄库，没有过期
        key_dict = {
            'ppid__in': self.id_list,
            'dppid': 0,
            'status':0,
            'invaliddate__gte': user.now_date,
        }
        res = self.PC.get_oddmentdrawnotes(False, *values_list, **key_dict)
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_oddmentdrawlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['batchno'])
            qtreeitem.setText(2, str(item['amount']))
            qtreeitem.setText(3, item['unit'])
            qtreeitem.setText(
                4, item['registerid'] + ' ' + item['registername']
            )
            qtreeitem.setText(5, str(item['regdate']))
            qtreeitem.setText(6, str(item['invaliddate']))
            qtreeitem.setCheckState(1, 0)
        for i in range(1, 7):
            self.treeWidget_oddmentdrawlist.resizeColumnToContents(i)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_oddmentdrawlist_itemDoubleClicked(self, qtreeitem, p_int):
        state = qtreeitem.checkState(1)
        if state == 0:
            qtreeitem.setCheckState(1, 2)
        else:
            qtreeitem.setCheckState(1, 0)
    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        it = QTreeWidgetItemIterator(self.treeWidget_oddmentdrawlist)
        select_id_list = []
        while it.value():
            qtreeitem = it.value()
            if qtreeitem.checkState(1) == 2:
                select_id_list.append(int(qtreeitem.text(0)))
            it += 1
        if not len(select_id_list):
            return
        detail = {
            'dppid': self.ppid,
            'drawerid': user.user_id,
            'drawername': user.user_name,
            'drawdate': user.now_date
        }
        res = self.PC.update_oddmentdrawnotes(select_id_list, **detail)
        if res:
            self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()