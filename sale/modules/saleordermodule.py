# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from sale.views.saleorder import Ui_Dialog

from sale.controllers.salecontroller import SaleController
from warehouse.controllers.warehousecontroller import WarehouseController
from workshop.controllers.workshopcontroller import WorkshopController
from sale.modules.editsaleprodmodule import EditSaleProdMudule
from sale.modules.editsaleordermodule import EditSaleOrderMudule

from django.db.models import Sum

from lib.utils.messagebox import MessageBox

import user


class SaleOrderModule(QDialog, Ui_Dialog):

    def __init__(self, autoid, parent=None):
        super(SaleOrderModule, self).__init__(parent)
        self.setupUi(self)
        self.SC = SaleController()
        self.WC = WarehouseController()
        self.WSC = WorkshopController()
        self.autoid = autoid
        self.get_order_list()
        self.get_product_list()

    def get_order_list(self):
        key_dict = {'autoid': self.autoid}
        order_list = self.SC.get_salenotes(
            False, *VALUES_TUPLE_ORDER ,**key_dict
        )
        if not len(order_list):
            return
        order = order_list[0]
        self.label_paperno.setText(order['paperno'])
        self.label_client.setText(order['clientid'] + ' ' + order['clientname'])
        self.label_linkman.setText(order['linkman'])
        self.label_telno.setText(order['telno'])
        self.label_saler.setText(order['salerid'] + ' ' + order['salername'])
        self.label_saledate.setText(str(order['saledate']))
        self.label_deliveryplace.setText(order['deliveryplace'])
        self.label_deliverydate.setText(str(order['deliverydate']))
        self.label_consignment.setText(
            order['consignmentid'] + ' ' + order['consignmentname']
        )
        self.label_remark.setText(order['remark'])

    def get_product_list(self):

        self.treeWidget_prodlist.clear()
        self.treeWidget_prodlist.hideColumn(0)
        key_dict = {'snid': self.autoid}
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

VALUES_TUPLE_OUTPUT = ('autoid',)
VALUES_TUPLE_OUTPUTDATE = ('qr0',)

VALUES_TUPLE_ORDER = (
    'paperno', 'clientid', 'clientname', 'saledate', 'creatorid',
    'creatorname', 'deliverydate', 'deliveryplace',
    'remark', 'salerid', 'salername',
    'consignmentid', 'consignmentname', 'linkman', 'telno'
)

VALUES_TUPLE_PROD = (
    'autoid', 'prodid', 'prodname', 'spec', 'package', 'spunit', 'saleamount'
)

VALUES_TUPLE_REP = (
    'prodid', 'prodname', 'spec', 'package'
)