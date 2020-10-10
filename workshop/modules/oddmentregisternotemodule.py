# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QDate, QPoint

from product.controllers.productcontroller import ProductController
from workshop.modules.modifyoddmentmodule import Modifyoddmentmodule

from workshop.views.oddmentregisternote import Ui_Form

import datetime

import user

ODDMENT_STATUS = ("已登记", "已发放", "已寄库", "已入库", "已过期")


class OddmentregisternoteModule(QWidget, Ui_Form):
    """ 零头登记记录
    autoid: 登记表的ppid
    flag: 零头的状态
        0：已登记
        1：已发放
        2：已寄库
        3：已入库
        4：已过期
    """

    def __init__(self, ppid, parent=None):
        super(OddmentregisternoteModule, self).__init__(parent)
        self.ppid = ppid

        self.setupUi(self)
        self.PC = ProductController()
        # 获取半成品信息
        self.get_oddmentreg()


    def get_oddmentreg(self):
        self.treeWidget_oddmentlist.clear()
        self.treeWidget_oddmentlist.hideColumn(0)
        values_tupe = (
            "autoid", "registerid", "registername", "regdate", "batchno",
            "amount", "unit", "invaliddate", "drawerid", "drawername",
            "drawdate", "qaid", "qaname", "qadate", "warehousemanid",
            "warehousemanname", "warehousedate", "flag"
        )
        key_dict = {
            'ppid': self.ppid
        }
        res = self.PC.get_oddmentdrawnotes(False, *values_tupe, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_oddmentlist)
                qtreeitem.setText(0, str(item['autoid']))
                qtreeitem.setText(1, str(item['regdate']))
                qtreeitem.setText(2, str(item['amount']))
                qtreeitem.setText(3, item['unit'])
                qtreeitem.setText(4, item['batchno'])
                qtreeitem.setText(
                    5, item['registerid'] + ' ' + item['registername']
                )
                qtreeitem.setText(6, str(item['invaliddate']))

                qtreeitem.setText(7, item['drawerid'] + ' ' + item['drawername'])
                qtreeitem.setText(8, str(item['drawdate'])  if type(
                    item['drawdate']) is datetime.date else '')

                qtreeitem.setText(9, item['qaid'] + ' ' + item['qaname'])
                qtreeitem.setText(10, str(item['qadate'])  if type(
                    item['qadate']) is datetime.date else '')

                qtreeitem.setText(
                    11, item['warehousemanid'] + ' ' + item['warehousemanname']
                )
                qtreeitem.setText(12, str(item['warehousedate']) if type(
                    item['warehousedate']) is datetime.date else '')
                qtreeitem.setText(13, ODDMENT_STATUS[item['flag']])

            for i in range(1, 14):
                self.treeWidget_oddmentlist.resizeColumnToContents(i)


    @pyqtSlot(QPoint)
    def on_treeWidget_oddmentlist_customContextMenuRequested(self, pos):
        sender_widget = self.sender()
        menu = QMenu()
        qtreeitem = sender_widget.currentItem()

        button1 = menu.addAction("增加")
        if qtreeitem is not None:
            button2 = menu.addAction("修改")
            button3 = menu.addAction("删除")
            button4 = menu.addAction("提交寄库")
            button5 = menu.addAction("取消寄库")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if qtreeitem is None:
            if action == button1:
                detail = Modifyoddmentmodule(ppid=self.ppid, parent=self)
                detail.exec()
        else:
            autoid = int(qtreeitem.text(0))
            if action == button1:
                detail = Modifyoddmentmodule(ppid=self.ppid, parent=self)
                detail.exec()
            elif action == button2:
                detail = Modifyoddmentmodule(autoid=autoid, ppid=self.ppid, parent=self)
                detail.exec()
            elif action == button3:
                self.PC.delete_oddmentdrawnotes(autoid=autoid)
            elif action == button4:
                flag = qtreeitem.text(13)
                if ODDMENT_STATUS.index(flag) == 0:
                    detail = {
                        'flag': 2,
                        'qaid': user.user_id,
                        'qaname': user.user_name,
                        'qadate': user.now_date
                    }
                    self.PC.update_oddmentdrawnotes(autoid=autoid, **detail)
            elif action == button5:
                flag = qtreeitem.text(13)
                if ODDMENT_STATUS.index(flag) == 2:
                    detail = {
                        'flag': 0,
                        'qaid': '',
                        'qaname': '',
                        'qadate': None
                    }
                    self.PC.update_oddmentdrawnotes(autoid=autoid, **detail)

        self.get_oddmentreg()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_oddmentlist_itemDoubleClicked(self, qtreeitem ,p_int):
        autoid = int(qtreeitem.text(0))
        detail = Modifyoddmentmodule(autoid=autoid, ppid=self.ppid, parent=self)
        detail.exec()
        self.get_oddmentreg()