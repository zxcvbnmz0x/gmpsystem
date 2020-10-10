# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu

from PyQt5.QtCore import pyqtSlot, QDate, QPoint

from product.controllers.productcontroller import ProductController

from workshop.views.oddmentdrawnote import Ui_Form
from workshop.modules.selectoddmentdrawmodule import SelectoddmentdrawModule

import datetime

import user

class OddmentdrawnoteModule(QWidget, Ui_Form):
    """ 半成品发放记录
    autoid: 发放表的ppid
    kind: 0为登记记录，1为发放记录
    """

    def __init__(self, ppid, parent=None):
        super(OddmentdrawnoteModule, self).__init__(parent)
        self.ppid = ppid
        self.setupUi(self)
        self.PC = ProductController()
        # 获取零头发放信息
        self.get_oddmentdraw()

    def get_oddmentdraw(self):
        self.treeWidget_oddmentlist.clear()
        self.treeWidget_oddmentlist.hideColumn(0)
        values_tupe = (
            "autoid", "registerid", "registername", "regdate", "batchno",
            "amount", "unit", "drawerid", "drawername", "drawdate"
        )
        key_dict = {
            'dppid': self.ppid
        }
        res = self.PC.get_oddmentdrawnotes(False, *values_tupe, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_oddmentlist)
                qtreeitem.setText(0, str(item['autoid']))
                qtreeitem.setText(
                    1, item['registerid'] + ' ' + item['registername']
                )
                qtreeitem.setText(2, str(item['regdate']))
                qtreeitem.setText(3, str(item['amount']))
                qtreeitem.setText(4, item['unit'])
                qtreeitem.setText(5, item['batchno'])
                qtreeitem.setText(
                    6, item['drawerid'] + ' ' + item['drawername']
                )
                qtreeitem.setText(7, str(item['drawdate']))


            for i in range(1, 8):
                self.treeWidget_oddmentlist.resizeColumnToContents(i)


    @pyqtSlot(QPoint)
    def on_treeWidget_oddmentlist_customContextMenuRequested(self, pos):
        sender_widget = self.sender()
        menu = QMenu()
        qtreeitem = sender_widget.currentItem()

        button1 = menu.addAction("增加")
        if qtreeitem is not None:
            button2 = menu.addAction("删除")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if qtreeitem is None:
            if action == button1:
                detail = SelectoddmentdrawModule(ppid=self.ppid, parent=self)
                detail.exec()
        else:
            autoid = int(qtreeitem.text(0))
            if action == button1:
                detail = SelectoddmentdrawModule(ppid=self.ppid, parent=self)
                detail.exec()
            elif action == button2:
                detail = {
                    'dppid': 0,
                    'drawerid': '',
                    'drawername': '',
                    'drawdate': ''
                }
                self.PC.update_oddmentdrawnotes(autoid=autoid, **detail)


        self.get_oddmentdraw()
