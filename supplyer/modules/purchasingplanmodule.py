# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu

from PyQt5.QtCore import pyqtSlot, QDate, QPoint

from supplyer.controllers.supplyercontroller import SupplyerController

from supplyer.modules.editpurchasingplanmodule import EditpurchasingplanModule
from supplyer.modules.editpurstuffmodule import EditpurstuffModule

from supplyer.views.purchasingplan import Ui_Form

from lib.utils.messagebox import MessageBox

import datetime

import user


class PurchasingplanModule(QWidget, Ui_Form):
    """ 采购计划表记录
    分3个标签，0：编辑状态；允许随意修改
            1：正在执行；只运行提交完成/退回编辑
            2：已完成；只能查看不能修改
    """

    def __init__(self, parent=None):
        super(PurchasingplanModule, self).__init__(parent)
        self.setupUi(self)
        self.SC = SupplyerController()
        self.ppid = None
        self.ori_detail = dict()
        self.new_detail = dict()
        self.groupBox.setVisible(False)
        # 获取当前状态的采购记录
        self.get_orderdetail()

    def get_orderdetail(self):
        self.treeWidget_orderlist.clear()
        self.treeWidget_orderlist.hideColumn(0)
        self.treeWidget_orderlist.hideColumn(1)

        index = self.tabWidget.currentIndex()
        key_dict_prod = {
                'status': index
            }

        res = self.SC.get_purchasingplan(
            False, *VALUES_TUPLE_ORDER, **key_dict_prod
        )
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_orderlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, str(item['spid']))
            qtreeitem.setText(2, item['paperno'])
            qtreeitem.setText(3, item['supid'] + ' ' + item['supname'])
            qtreeitem.setText(4, str(item['createdate']))
            qtreeitem.setText(5, item['creatorid'] + ' ' + item['creatorname'])
            qtreeitem.setText(
                6, item['warrantorid'] + ' ' + item['warrantorname']
            )
            qtreeitem.setText(7, str(item['invaliddate']))
            qtreeitem.setText(8, item['remark'])

        for i in range(2, 9):
            self.treeWidget_orderlist.resizeColumnToContents(i)

    # 获取物料信息
    def get_stuffdetail(self):
        self.treeWidget_stufflist.clear()
        self.treeWidget_stufflist.hideColumn(0)
        key_dict = {
            'ppid': self.ppid
        }
        res = self.SC.get_purchstuff(
            False, *VALUES_TUPLE_STUFF, **key_dict
        )
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_stufflist)
                qtreeitem.setText(0, str(item['autoid']))
                qtreeitem.setText(1, item['stuffid'] + ' ' + item['stuffname'])
                qtreeitem.setText(2, STUFF_TYPE[item['stufftype']])
                qtreeitem.setText(3, item['spec'])
                qtreeitem.setText(4, item['package'])
                qtreeitem.setText(5, str(item['amount']))
                qtreeitem.setText(6, str(item['arrivedamount']))
                qtreeitem.setText(7, item['unit'])
                qtreeitem.setText(8, item['producer'])

            for i in range(1, 9):
                self.treeWidget_stufflist.resizeColumnToContents(i)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        getattr(self, 'tab_' + str(p_int)).setLayout(self.gridLayout_2)
        self.get_orderdetail()
        self.groupBox.setVisible(False)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemClicked(self, qtreeitem, p_int):
        if not self.groupBox.isVisible():
            self.groupBox.setVisible(True)
        self.ppid = int(qtreeitem.text(0))
        self.get_stuffdetail()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemDoubleClicked(self, qtreeitem, p_int):
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
        id = int(qtreeitem.text(0))
        detail = EditpurchasingplanModule(id, self)
        detail.accepted.connect(self.get_orderdetail)
        detail.show()

    @pyqtSlot(QPoint)
    def on_treeWidget_orderlist_customContextMenuRequested(self, pos):
        id = 0
        index = self.tabWidget.currentIndex()
        if index == 2:
            return
            # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is not None:
            id = int(current_item.text(0))
        menu = QMenu()
        if index == 0:
            button1 = menu.addAction("新增计划单")
            button2 = menu.addAction("修改计划单")
            button3 = menu.addAction("删除计划单")
            button4 = menu.addAction("提交执行")
        elif index == 1:
            button5 = menu.addAction("完成计划单")
            button6 = menu.addAction("退回编辑")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if index == 0:
            if action == button1:
                detail = EditpurchasingplanModule(None, self)
                detail.accepted.connect(self.get_orderdetail)
                detail.show()
            elif action == button2:
                detail = EditpurchasingplanModule(id, self)
                detail.accepted.connect(self.get_orderdetail)
                detail.show()
            elif action == button3:
                if id is None:
                    return
                key_dict = {
                    'ppid': id
                }
                self.SC.delete_purchstuff(**key_dict)
                self.SC.delete_purchasingplan(id)
            elif action == button4:
                if id is None:
                    return
                warrantor = current_item.text(5)
                if warrantor in ('', ' '):
                    message = MessageBox(
                        self, text="无法提交执行", informative="批准人还没有签名"
                    )
                    message.show()
                    return
                key_dict = {
                    'status': 1
                }
                self.SC.update_purchasingplan(id, **key_dict)

        elif index == 1:
            if action == button5:
                if id is None:
                    return
                key_dict = {
                    'status': 2
                }
                self.SC.update_purchasingplan(id, **key_dict)
            elif action == button6:
                if id is None:
                    return
                key_dict = {
                    'status': 0
                }
                self.SC.update_purchasingplan(id, **key_dict)
        self.get_orderdetail()

    @pyqtSlot(QPoint)
    def on_treeWidget_stufflist_customContextMenuRequested(self, pos):
        id = []
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
        order_item = self.treeWidget_orderlist.currentItem()
        if order_item is None:
            return
        ppid = order_item.text(0)
        spid = order_item.text(1)
        # 返回调用者的对象
        sender_widget = self.sender()
        select_items = sender_widget.selectedItems()
        if select_items is not None:
            for item in select_items:
                id.append(int(item.text(0)))
        menu = QMenu()

        button1 = menu.addAction("新增物料")
        button2 = menu.addAction("修改物料")
        button3 = menu.addAction("删除物料")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:

            detail = EditpurstuffModule(spid, ppid, None, self)
            detail.accepted.connect(self.get_stuffdetail)
            detail.show()
        elif action == button2:
            current_item = sender_widget.currentItem()
            current_id = int(current_item.text(0))
            detail = EditpurchasingplanModule(spid, None, current_id, self)
            detail.accepted.connect(self.get_stuffdetail)
            detail.show()
        elif action == button3:
            if id is None:
                return
            key_dict = {
                'autoid__in': id
            }
            self.SC.delete_purchstuff(**key_dict)

        self.get_stuffdetail()

VALUES_TUPLE_ORDER = (
    "autoid", "paperno", "createdate", "creatorid", "creatorname", "spid",
    "supid", "supname", "warrantorid", "warrantorname", "remark", "invaliddate"
)

VALUES_TUPLE_STUFF = (
            "autoid", "stuffid", "stuffname", "stufftype", "spec", "package",
            "amount", "arrivedamount", "unit", "producer"
        )
STUFF_TYPE = ("主材料", "前处理", "辅材料", "内包材", "外包材")