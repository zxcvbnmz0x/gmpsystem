# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu, \
    QTreeWidgetItemIterator

from PyQt5.QtCore import pyqtSlot, QDate, QPoint

from product.controllers.productcontroller import ProductController

from workshop.modules.modifymiddetailmodule import Modifymiddetailmodule
from lib.sign.signmodule import SignModule

from workshop.views.midproddetail import Ui_Form

import datetime

import user


class MidproddetailModule(QWidget, Ui_Form):
    """ 半成品登记/发放列表记录记录
    分3个标签，0：未登记，1：已登记，2：已发放
    点击其中一条生产记录时下方显示对应的记录内容
    在未登记标签里右键可以选择增加新的登记信息，以及工人签名
    在已登记标签里右键可以选中发放签名以及工人签名
    """

    def __init__(self, parent=None):
        super(MidproddetailModule, self).__init__(parent)
        self.setupUi(self)
        self.ppid = 0
        self.sign_id = ''
        self.sign_name = ''
        self.PC = ProductController()
        self.ori_detail = dict()
        self.new_detail = dict()
        self.groupBox.setVisible(False)

        # 获取当前状态的批生产记录
        self.get_prodstatusinmid()

    def get_prodstatusinmid(self):
        self.treeWidget_prodlist.clear()
        values_tuple = (
            "autoid", "prodid", "prodname", "commonname", "spec", "package",
            "planamount", "basicunit"
        )
        index = self.tabWidget.currentIndex()
        key_dict = {
            'midstatus': index
        }
        res = self.PC.get_producingplan(False, *values_tuple, **key_dict)
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_prodlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['prodid'] + ' ' + item['prodname'])
            qtreeitem.setText(2, item['commonname'])
            qtreeitem.setText(3, item['spec'])
            qtreeitem.setText(4, item['package'])
            qtreeitem.setText(5, str(item['planamount']) + item['basicunit'])
        self.treeWidget_prodlist.hideColumn(0)
        for i in range(1, 6):
            self.treeWidget_prodlist.resizeColumnToContents(i)

    # 获取半成品信息
    def get_midprod(self):
        self.treeWidget_midprodlist.clear()
        values_list = [
            "autoid", "container", "amount", "unit", "registrarid",
            "registrarname", "regtime", "workerid", "workername", "providerid",
            "providername", "drawtime", "drawerid", "drawername"]

        key_dict = {
            'ppid': self.ppid
        }
        res = self.PC.get_midproddrawnotes(True, *values_list, **key_dict)
        if len(res):
            for item in res.order_by('container'):
                qtreeitem = QTreeWidgetItem(self.treeWidget_midprodlist)
                qtreeitem.setText(0, str(item[0]))  # autoid
                qtreeitem.setText(1, str(item[1]))  # 桶号
                qtreeitem.setText(2, str(item[2]) + item[3])  # 数量
                qtreeitem.setText(3, item[4] + ' ' + item[5])  # 登记人
                qtreeitem.setText(4, str(item[6]))  # 登记日期
                qtreeitem.setText(5, item[7] + ' ' + item[8])  # 登记工人
                qtreeitem.setText(6, item[9] + ' ' + item[10])  # 发放人
                qtreeitem.setText(7, str(item[11]) if type(
                    item[11]) is datetime.datetime else '')  # 发放日期
                qtreeitem.setText(8, item[12] + ' ' + item[13])  # 领取工人

            self.treeWidget_midprodlist.hideColumn(0)
            for i in range(1, 6):
                self.treeWidget_midprodlist.resizeColumnToContents(i)

    # @pyqtSlot()
    # def on_pushButton_workersign_clicked(self):
    #     it = QTreeWidgetItemIterator(self.treeWidget_midproductlist)
    #
    #     id_list = []
    #     while it.value():
    #         item = it.value()
    #         id_list.append(int(item.text(0)))
    #         it += 1
    #     if not len(id_list):
    #         return
    #     detail = dict()
    #     status : int
    #     if self.kind == 0:
    #         detail = {
    #             'workerid': user.user_id,
    #             'workername': user.user_name
    #         }
    #         status = 1
    #     elif self.kind == 1:
    #         detail = {
    #             'drawerid': user.user_id,
    #             'drawername': user.user_name
    #         }
    #         status = 2
    #
    #     res = self.PC.update_midproddrawnotes(id_list, self.autoid, status, **detail)
    #     if res > 0:
    #         self.get_midprod()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        getattr(self, 'tab_' + str(p_int)).setLayout(self.gridLayout_2)
        self.get_prodstatusinmid()
        self.groupBox.setVisible(False)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_prodlist_itemClicked(self, qtreeitem, p_int):
        if not self.groupBox.isVisible():
            self.groupBox.setVisible(True)
        self.ppid = int(qtreeitem.text(0))
        self.get_midprod()

    @pyqtSlot(QPoint)
    def on_treeWidget_midprodlist_customContextMenuRequested(self, pos):
        # 返回调用者的对象
        sender_widget = self.sender()
        menu = QMenu()
        index = self.tabWidget.currentIndex()
        if index == 0:
            button1 = menu.addAction("增加")
            button2 = menu.addAction("修改")
            button3 = menu.addAction("删除")
            button4 = menu.addAction("登记工人签名")

        elif index == 1:
            button5 = menu.addAction("发放人签名")
            button6 = menu.addAction("领取工人签名")
        else:
            return

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if index == 0:
            if action == button1:
                ppid = int(self.treeWidget_prodlist.currentItem().text(0))
                detail = Modifymiddetailmodule(ppid=ppid, parent=self)
                detail.itemAdded.connect(self.get_midprod)
                detail.show()
            elif action == button2:
                qtreeitem = sender_widget.currentItem()
                if not qtreeitem:
                    return
                detail = Modifymiddetailmodule(autoid=int(qtreeitem.text(0)),
                                               parent=self)
                detail.accepted.connect(self.get_midprod)
                detail.show()
            elif action == button3:
                items = sender_widget.selectedItems()
                if not items:
                    return
                id_list = []
                for item in items:
                    id_list.append(int(item.text(0)))
                res = self.PC.delete_midproddrawnotes(id_list)
                if res:
                    self.get_midprod()
            elif action == button4:
                signmodule = SignModule()
                signmodule.userchanged.connect(self.set_signuser)
                signmodule.exec()
                id_list = []
                it = QTreeWidgetItemIterator(self.treeWidget_midprodlist)
                while it.value():
                    qtreeitem = it.value()
                    id_list.append(int(qtreeitem.text(0)))
                    it += 1
                detail = {
                    'workerid': self.sign_id,
                    'workername': self.sign_name
                }
                if not len(id_list):
                    return
                res = self.PC.update_midproddrawnotes(
                    autoid=id_list, pid=self.ppid, **detail, status=1
                )
                if res:
                    self.get_midprod()
                    self.get_prodstatusinmid()
        elif index == 1:
            if action == button5:
                signmodule = SignModule()
                signmodule.userchanged.connect(self.set_signuser)
                signmodule.exec()
                id_list = []
                it = QTreeWidgetItemIterator(self.treeWidget_midprodlist)
                while it.value():
                    qtreeitem = it.value()
                    id_list.append(int(qtreeitem.text(0)))
                    it += 1
                detail = {
                    'providerid': self.sign_id,
                    'providername': self.sign_name,
                    'drawtime': user.time
                }
                if not len(id_list):
                    return
                res = self.PC.update_midproddrawnotes(autoid=id_list, **detail)
                if res:
                    self.get_midprod()
                    self.get_prodstatusinmid()
            elif action == button6:
                signmodule = SignModule()
                signmodule.userchanged.connect(self.set_signuser)
                signmodule.exec()
                id_list = []
                it = QTreeWidgetItemIterator(self.treeWidget_midprodlist)
                while it.value():
                    qtreeitem = it.value()
                    if qtreeitem.text(6) not in ('', ' '):
                        id_list.append(int(qtreeitem.text(0)))
                    it += 1
                detail = {
                    'drawerid': self.sign_id,
                    'drawername': self.sign_name
                }
                if not len(id_list):
                    return
                if len(
                        id_list) < self.treeWidget_midprodlist.topLevelItemCount() \
                        or self.sign_id in ('', ' '):
                    status = 1
                else:
                    status = 2
                res = self.PC.update_midproddrawnotes(
                    autoid=id_list, pid=self.ppid, **detail, status=status
                )
                if res:
                    self.get_midprod()
                    self.get_prodstatusinmid()
        # except (AttributeError， UnboundLocalError):
        # pass

    def set_signuser(self, p_str):
        if p_str in ('', ' '):
            self.sign_id = ''
            self.sign_name = ''
        else:
            try:
                self.sign_id, self.sign_name = p_str.split(' ')
            except ValueError:
                self.sign_id = ''
                self.sign_name = ''

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_midprodlist_itemDoubleClicked(self, qtreeitem, p_int):
        if not qtreeitem:
            return
        detail = Modifymiddetailmodule(
            autoid=int(qtreeitem.text(0)), parent=self
        )
        detail.accepted.connect(self.get_midprod)
        detail.show()
