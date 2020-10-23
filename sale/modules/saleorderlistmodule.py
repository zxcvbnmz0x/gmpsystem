# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from sale.views.saleorderlist import Ui_Form

from sale.controllers.salecontroller import SaleController
from warehouse.controllers.warehousecontroller import WarehouseController
from workshop.controllers.workshopcontroller import WorkshopController
from sale.modules.editsaleprodmodule import EditSaleProdMudule
from sale.modules.editsaleordermodule import EditSaleOrderMudule

from django.db.models import Sum

from lib.utils.messagebox import MessageBox

import user


class SaleOrderListModule(QWidget, Ui_Form):

    def __init__(self, parent=None):
        super(SaleOrderListModule, self).__init__(parent)
        self.setupUi(self)
        self.SC = SaleController()
        self.WC = WarehouseController()
        self.WSC = WorkshopController()
        self.groupBox.setVisible(False)
        self.snid = 0
        self.get_order_list()

    def get_order_list(self):
        self.treeWidget_orderlist.clear()
        self.treeWidget_orderlist.hideColumn(0)
        index = self.tabWidget.currentIndex()
        key_dict = {'status': index}
        order_list = self.SC.get_salenotes(
            False, *VALUES_TUPLE_ORDER ,**key_dict
        )
        if not len(order_list):
            return
        for item in order_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_orderlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['paperno'])
            qtreeitem.setText(2, item['clientid'] + ' ' + item['clientname'])
            qtreeitem.setText(3, item['linkman'])
            qtreeitem.setText(4, item['telno'])
            qtreeitem.setText(5, str(item['saledate']))
            qtreeitem.setText(6, str(item['deliverydate']))
            qtreeitem.setText(7, item['deliveryplace'])
            qtreeitem.setText(8, item['salerid'] + ' ' + item['salername'])
            qtreeitem.setText(9, item['conveyance'])
            qtreeitem.setText(10, item['paymethod'])
            qtreeitem.setText(
                11, item['consignmentid'] + ' ' + item['consignmentname']
            )
            qtreeitem.setText(12, item['deliverid'] + ' ' + item['delivername'])
            qtreeitem.setText(13, item['remark'])
        for i in range(1, 14):
            self.treeWidget_orderlist.resizeColumnToContents(i)

    def get_product_list(self):

        self.treeWidget_prodlist.clear()
        self.treeWidget_prodlist.hideColumn(0)
        key_dict = {'snid': self.snid}
        prod_list = self.SC.get_salenotegoods(
            False, *VALUES_TUPLE_PROD ,**key_dict
        )
        if not len(prod_list):
            return
        for item in prod_list:
            qtreeitem = QTreeWidgetItem(self.treeWidget_prodlist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['prodid'] + ' ' + item['prodname'])
            qtreeitem.setText(2, item['spec'])
            qtreeitem.setText(3, item['package'])
            qtreeitem.setText(4, str(item['saleamount'].to_integral()))
            qtreeitem.setText(5, item['spunit'])
            prodid = item['prodid']
            key_dict_rep = {
                'prodid': prodid,
                'stockamount__gt': 0
            }
            product_rep_list = self.WC.get_productrepository(
                False, *VALUES_TUPLE_REP, **key_dict_rep
            ).annotate(amount=Sum('stockamount'))
            if len(product_rep_list):
                qtreeitem.setText(
                    6, str(product_rep_list[0]['amount'].to_integral())
                )
            else:
                qtreeitem.setText(6, '0')
        for i in range(1, 7):
            self.treeWidget_prodlist.resizeColumnToContents(i)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        tab = getattr(self, 'tab_' + str(p_int))
        tab.setLayout(self.gridLayout_2)
        self.groupBox.setVisible(False)
        self.get_order_list()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemClicked(self, qtreeitem, p_int):
        self.groupBox.setVisible(True)

        self.snid = int(qtreeitem.text(0))
        self.get_product_list()

    @pyqtSlot(QPoint)
    def on_treeWidget_orderlist_customContextMenuRequested(self, pos):
        id = 0
        index = self.tabWidget.currentIndex()
            # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is not None:
            id = int(current_item.text(0))

        menu = QMenu()
        if index == 0:
            button1 = menu.addAction("新增销售单")
            button2 = menu.addAction("修改销售单")
            button3 = menu.addAction("删除销售单")
            button4 = menu.addAction("提交审核")
        elif index == 1:
            button5 = menu.addAction("审核签名")
            button6 = menu.addAction("取消提交")
        elif index == 2:
            button7 = menu.addAction("取消发货")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if index == 0:
            if action == button1:
                detail = EditSaleOrderMudule(parent=self)
                detail.accepted.connect(self.get_order_list)
                detail.show()
            elif action == button2:
                if id is None:
                    return
                detail = EditSaleOrderMudule(id , self)
                detail.accepted.connect(self.get_order_list)
                detail.show()
            elif action == button3:
                if id is None:
                    return

                key_dict_output = {
                    'snid': id
                }
                res = self.WC.get_productputoutpaper(
                    True, *VALUES_TUPLE_OUTPUT, **key_dict_output
                )
                if len(res):
                    key_dict_qrcode = {'ppopid': res[0]}
                    qrcodelist = self.WC.get_ppopqrcode(
                        True, *VALUES_TUPLE_OUTPUTDATE, **key_dict_qrcode
                    )
                    if len(qrcodelist):
                        msg = MessageBox(self, text="已有出库记录，无法取消发货！")
                        msg.show()
                key_dict = {
                    'snid': id
                }
                self.SC.delete_salenotes(id)
                self.SC.delete_salenotegoods(**key_dict)
                self.WC.delete_productputoutpaper(**key_dict)
                self.get_order_list()
            elif action == button4:
                if id is None:
                    return
                key_dict = {
                    'status': 1
                }
                self.SC.update_salenotes(id, **key_dict)
                self.get_order_list()
        elif index == 1:
            if action == button5:
                if id is None:
                    return
                key_dict = {
                    'consignmentid': user.user_id,
                    'consignmentname': user.user_name,
                    'status': 2
                }
                self.SC.update_salenotes(id, **key_dict)
                key_dict_output = {
                    'snid': id
                }
                res = self.WC.get_productputoutpaper(
                    False, *VALUES_TUPLE_OUTPUT, **key_dict_output
                )
                if not len(res):
                    output_detail = {
                        'snid': id,
                        'snpaperno': current_item.text(1),
                        'pokind': "销售出库",
                        'clientid': current_item.text(2).split(' ')[0],
                        'clientname': current_item.text(2).split(' ')[1],
                        'remark': current_item.text(13)
                    }
                    res = self.WC.update_productputoutpaper(**output_detail)
                self.get_order_list()
            elif action == button6:
                if id is None:
                    return
                key_dict = {
                    'consignmentid': '',
                    'consignmentname': '',
                    'status': 0
                }
                self.SC.update_salenotes(id, **key_dict)
                self.get_order_list()
        elif index == 2:
            if action == button7:
                if id is None:
                    return
                key_dict = {
                    'consignmentid': '',
                    'consignmentname': '',
                    'status': 1
                }
                self.SC.update_salenotes(id, **key_dict)
                self.get_order_list()



    @pyqtSlot(QPoint)
    def on_treeWidget_prodlist_customContextMenuRequested(self, pos):
        id = 0
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
            # 返回调用者的对象
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        if current_item is not None:
            id = int(current_item.text(0))

        menu = QMenu()
        button1 = menu.addAction("增加")
        button2 = menu.addAction("修改")
        button3 = menu.addAction("删除")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if action == button1:
            detail = EditSaleProdMudule(snid=self.snid,parent=self)
            detail.accepted.connect(self.get_product_list)
            detail.show()

        elif action == button2:
            if not id:
                return
            detail = EditSaleProdMudule(autoid=id, parent=self)
            detail.accepted.connect(self.get_product_list)
            detail.show()
        elif action == button3:
            if not id:
                return
            key_dict_prod = {'autoid': id}
            lab_list = self.SC.delete_salenotegoods(**key_dict_prod)
            self.get_product_list()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_orderlist_itemDoubleClicked(self, qtreeitem, p_int):
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
        id = int(qtreeitem.text(0))
        detail = EditSaleOrderMudule(autoid=id, parent=self)
        detail.accepted.connect(self.get_order_list)
        detail.show()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_prodlist_itemDoubleClicked(self, qtreeitem, p_int):
        index = self.tabWidget.currentIndex()
        if index != 0:
            return
        id = int(qtreeitem.text(0))
        detail = EditSaleProdMudule(autoid=id, parent=self)
        detail.accepted.connect(self.get_product_list)
        detail.show()

VALUES_TUPLE_OUTPUT = ('autoid',)
VALUES_TUPLE_OUTPUTDATE = ('qr0',)

VALUES_TUPLE_ORDER = (
    'autoid', 'paperno', 'clientid', 'clientname', 'saledate', 'creatorid',
    'creatorname', 'deliverydate', 'deliveryplace', 'conveyance', 'paymethod',
    'remark', 'deliverid', 'delivername', 'salerid', 'salername',
    'consignmentid', 'consignmentname', 'linkman', 'telno'
)

VALUES_TUPLE_PROD = (
    'autoid', 'prodid', 'prodname', 'spec', 'package', 'spunit', 'saleamount'
)

VALUES_TUPLE_REP = (
    'prodid', 'prodname', 'spec', 'package'
)