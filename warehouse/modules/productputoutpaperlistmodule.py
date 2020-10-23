# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from warehouse.views.productputoutpaperlist import Ui_Form

from sale.controllers.salecontroller import SaleController
from warehouse.controllers.warehousecontroller import WarehouseController
from workshop.controllers.workshopcontroller import WorkshopController
from warehouse.modules.editproductputoutpapermodule import EditProductPutOutPaperModule
from warehouse.modules.scanppopqrcodemodule import ScanPpopQrcodeMudule
from sale.modules.saleordermodule import SaleOrderModule

from django.db.models import Sum

from lib.utils.messagebox import MessageBox

import datetime

import user


class ProductPutOutPaperListModule(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(ProductPutOutPaperListModule, self).__init__(parent)
        self.setupUi(self)
        self.SC = SaleController()
        self.WC = WarehouseController()
        self.WSC = WorkshopController()
        self.groupBox.setVisible(False)
        self.ppopid = 0
        self.get_order_list()

    def get_order_list(self):
        self.treeWidget_orderlist.clear()
        # self.treeWidget_orderlist.hideColumn(0)
        # self.treeWidget_orderlist.hideColumn(1)
        index = self.tabWidget.currentIndex()
        key_dict = {'status': index}
        order_list = self.WC.get_productputoutpaper(
            False, *VALUES_TUPLE_ORDER, **key_dict
        )
        if not len(order_list):
            return
        for item in order_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_orderlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, str(item['snid']))
            qtreeitem.setText(2, item['snpaperno'])
            qtreeitem.setText(3, item['pokind'])
            qtreeitem.setText(
                4, str(item['putoutdate']) if type(
                    item['putoutdate']) is datetime.date else ''
            )
            qtreeitem.setText(5, item['clientid'] + ' ' + item['clientname'])
            qtreeitem.setText(6, item['auditorid'] + ' ' + item['auditorname'])
            qtreeitem.setText(7, str(item['remark']))

        for i in range(2, 8):
            self.treeWidget_orderlist.resizeColumnToContents(i)

    def get_qrcode_list(self):

        self.treeWidget_itemlist.clear()
        self.treeWidget_itemlist.hideColumn(0)
        key_dict = {'ppopid': self.ppopid}
        prod_list = self.WC.get_ppopqrcode(
            False, **key_dict
        ).extra(
            select={
                'prodid': 'prodid', 'prodname': 'prodname', 'spec': 'spec',
                'package': 'package', 'lpunit': 'lpunit', 'bpunit': 'bpunit',
                'mpunit': 'mpunit', 'spunit': 'spunit'
            },
            tables=['producingplan'],
            where=['ppid=producingplan.autoid']
        ).values(*VALUES_TUPLE_PROD)
        if not len(prod_list):
            return
        for item in prod_list:
            package_unit = [
                item['spunit'], item['mpunit'], item['bpunit'], item['lpunit']
            ]
            qtreeitem = QTreeWidgetItem(self.treeWidget_itemlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, KIND[item['kind']])
            qtreeitem.setText(2, item['prodid'] + ' ' + item['prodname'])
            qtreeitem.setText(3, item['batchno'])
            qtreeitem.setText(4, str(item['amount']) + item['spunit'])
            qtreeitem.setText(5, item['spec'])
            qtreeitem.setText(6, item['package'])
            qtreeitem.setText(7, item['qr0'])
            qtreeitem.setText(8, package_unit[item['flag']] + '码')

        for i in range(1, 9):
            self.treeWidget_itemlist.resizeColumnToContents(i)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        tab = getattr(self, 'tab_' + str(p_int))
        tab.setLayout(self.gridLayout_2)
        self.groupBox.setVisible(False)
        self.get_order_list()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemClicked(self, qtreeitem, p_int):
        self.groupBox.setVisible(True)

        self.ppopid = int(qtreeitem.text(0))
        self.get_qrcode_list()

    @pyqtSlot(QPoint)
    def on_treeWidget_orderlist_customContextMenuRequested(self, pos):
        id = 0
        snid = 0
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
        # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is not None:
            id = int(current_item.text(0))
            snid = int(current_item.text(1))

        menu = QMenu()

        button1 = menu.addAction("新增出库单")
        button2 = menu.addAction("修改出库单")
        button3 = menu.addAction("删除出库单")
        menu.addSeparator()
        button4 = menu.addAction("提交出库")
        menu.addSeparator()
        button5 = menu.addAction("查看销售订单")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = EditProductPutOutPaperModule(parent=self)
            detail.accepted.connect(self.get_order_list)
            detail.show()
        elif action == button2:
            if id is None:
                return
            detail = EditProductPutOutPaperModule(id, self)
            detail.accepted.connect(self.get_order_list)
            detail.show()
        elif action == button3:
            if id is None:
                return

            key_dict_output = {'ppopid': id}
            res = self.WC.get_ppopqrcode(
                True, *VALUES_TUPLE_OUTPUT, **key_dict_output
            )
            if len(res):
                msg = MessageBox(self, text="已有出库记录，无法删除出库单！")
                msg.show()
                return

            key_dict = {'autoid': id}
            self.WC.delete_productputoutpaper(**key_dict)
            self.get_order_list()
        elif action == button4:
            if id is None:
                return
            key_dict = {
                'status': 1,
                'auditorid': user.user_id,
                'auditorname': user.user_name
            }
            res = self.WC.apply_productputoutpaper(id, snid, **key_dict)
            print(res)
            if snid != 0:
                key_dict_salenote = {
                    'status': 3,
                    'deliverid': user.user_id,
                    'delivername': user.user_name
                }
                self.SC.update_salenotes(snid, **key_dict_salenote)
            self.get_order_list()
        elif action == button5:
            if snid == 0:
                msg = MessageBox(self, text="没有找到关联的销售订单")
                msg.show()
                return
            detail = SaleOrderModule(snid, self)
            detail.show()

    @pyqtSlot(QPoint)
    def on_treeWidget_itemlist_customContextMenuRequested(self, pos):
        id = 0
        flag = 0
        qrcode = ''
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
            # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is not None:
            id = int(current_item.text(0))
            flag = int(current_item.text(1))
            qrcode = current_item.text(8)

        menu = QMenu()
        button1 = menu.addAction("增加")
        button2 = menu.addAction("删除")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = ScanPpopQrcodeMudule(self.ppopid, self)
            detail.qrcodeAdded.connect(self.get_qrcode_list)
            detail.show()

        elif action == button2:
            if not id:
                return
            self.WC.drop_ppopqrocde(flag, qrcode, id)
            self.get_qrcode_list()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemDoubleClicked(self, qtreeitem, p_int):
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
        id = int(qtreeitem.text(0))
        detail = EditProductPutOutPaperModule(autoid=id, parent=self)
        detail.accepted.connect(self.get_order_list)
        detail.show()


VALUES_TUPLE_OUTPUT = ('autoid',)
VALUES_TUPLE_OUTPUTDATE = ('qr0',)

VALUES_TUPLE_ORDER = (
    'autoid', 'snid', 'snpaperno', 'clientid', 'clientname',
    'pokind', 'auditorid', 'auditorname', 'putoutdate', 'remark'
)

VALUES_TUPLE_PROD = (
    'autoid', 'prodid', 'prodname', 'spec', 'package', 'lpunit', 'bpunit',
    'mpunit', 'spunit', 'batchno', 'qr0', 'flag', 'amount' , 'kind'
)

VALUES_TUPLE_REP = (
    'prodid', 'prodname', 'spec', 'package'
)
QRCODE_KIND = ('qrcode0', 'qrcode1', 'qrcode2', 'qrcode3')

KIND = ('普通', '零头', '合箱')