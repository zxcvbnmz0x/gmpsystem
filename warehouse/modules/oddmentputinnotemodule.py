# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu, \
    QTreeWidgetItemIterator

from PyQt5.QtCore import pyqtSlot, QDate, QPoint

from product.controllers.productcontroller import ProductController

from warehouse.views.oddmentputinnote import Ui_Form

import datetime

import user


class OddmentputinnoteModule(QWidget, Ui_Form):
    """ 零头登记/发放列表记录记录
    分6个标签，0：全部批记录，包括没有零头记录的批次；
            1：登记中；
            2：已发放；
            3：已寄库
            4：已入库
            5：已过期
    点击其中一条生产记录时下方显示对应的记录内容
    除了已过期标签下的零头记录外，其他的都没有功能，只允许查看
    """

    def __init__(self, parent=None):
        super(OddmentputinnoteModule, self).__init__(parent)
        self.setupUi(self)
        self.ppid = 0
        self.PC = ProductController()
        self.ori_detail = dict()
        self.new_detail = dict()
        self.groupBox.setVisible(False)
        # 获取当前状态的批生产记录
        self.get_proddetail()

    def get_proddetail(self):
        self.treeWidget_prodlist.clear()
        self.treeWidget_prodlist.hideColumn(0)

        values_tuple_prod = (
            "autoid", "prodid", "prodname", "commonname", "spec", "package",
            "planamount", "basicunit"
        )
        index = self.tabWidget.currentIndex()
        key_dict_prod = dict()
        key_dict_oddment = {
            'flag': index + 2
        }
        values_list_oddment = ['ppid']

        id_list = self.PC.get_oddmentdrawnotes(
            True, *values_list_oddment, **key_dict_oddment
        )
        if not len(id_list):
            return
        key_dict_prod['autoid__in'] = id_list.distinct()

        res = self.PC.get_producingplan(
            False, *values_tuple_prod, **key_dict_prod
        )
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_prodlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['prodid'] + ' ' + item['prodname'])
            qtreeitem.setText(2, item['commonname'])
            qtreeitem.setText(3, item['spec'])
            qtreeitem.setText(4, item['package'])
            qtreeitem.setText(5, str(item['planamount']) + item['basicunit'])

        for i in range(1, 6):
            self.treeWidget_prodlist.resizeColumnToContents(i)

    # 获取零头信息
    def get_oddmentdetail(self):
        self.treeWidget_oddmentlist.clear()
        self.treeWidget_oddmentlist.hideColumn(0)
        values_list = (
            "autoid", "amount", "unit", "registerid", "registername",
            "regdate", "invaliddate", "qaid", "qaname", "qadate",
            "warehousemanid", "warehousemanname", "warehousedate"
        )

        key_dict = {
            'ppid': self.ppid
        }
        index = self.tabWidget.currentIndex()
        key_dict['flag'] = index + 2
        res = self.PC.get_oddmentdrawnotes(False, *values_list, **key_dict)
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_oddmentlist)
                qtreeitem.setText(0, str(item['autoid']))  # autoid
                qtreeitem.setText(1, str(item['amount']))  # 数量
                qtreeitem.setText(2, item['unit'])  # 单位
                qtreeitem.setText(
                    3, item['registerid'] + ' ' + item['registername']
                )  # 登记人
                qtreeitem.setText(4, str(item['regdate']))  # 登记日期
                qtreeitem.setText(5, str(item['invaliddate']))  # 过期日期

                qtreeitem.setText(
                    6, item['qaid'] + ' ' + item['qaname']
                )  # 寄库人
                qtreeitem.setText(7, str(item['qadate']) if type(
                    item['qadate']) is datetime.date else '')  # 寄库日期
                qtreeitem.setText(
                    8, item['warehousemanid'] + ' ' + item['warehousemanname']
                )  # 入库人
                qtreeitem.setText(9, str(item['warehousedate']) if type(
                    item['warehousedate']) is datetime.date else '')  # 入库日期

            for i in range(1, 10):
                self.treeWidget_oddmentlist.resizeColumnToContents(i)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        getattr(self, 'tab_' + str(p_int)).setLayout(self.gridLayout_2)
        self.get_proddetail()
        self.groupBox.setVisible(False)


    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_prodlist_itemClicked(self, qtreeitem, p_int):
        if not self.groupBox.isVisible():
            self.groupBox.setVisible(True)
        self.ppid = int(qtreeitem.text(0))
        self.get_oddmentdetail()

    @pyqtSlot(QPoint)
    def on_treeWidget_oddmentlist_customContextMenuRequested(self, pos):
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
        # 返回调用者的对象
        sender_widget = self.sender()
        select_items = sender_widget.selectedItems()
        if not len(select_items):
            return
        id_list = []
        for item in select_items:
            id_list.append(int(item.text(0)))

        menu = QMenu()
        button1 = menu.addAction("确认寄库")
        button2 = menu.addAction("取消寄库")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = {
                'flag': 3,
                'warehousemanid': user.user_id,
                'warehousemanname': user.user_name,
                'warehousedate': user.now_date
            }
            self.PC.update_oddmentdrawnotes(id_list, **detail)

            self.get_proddetail()
            self.get_oddmentdetail()
        elif action == button2:
            detail = {
                'flag': 0,
                'qaid': '',
                'qaname': '',
                'qadate': None
            }
            self.PC.update_oddmentdrawnotes(id_list, **detail)

            self.get_proddetail()
            self.get_oddmentdetail()
