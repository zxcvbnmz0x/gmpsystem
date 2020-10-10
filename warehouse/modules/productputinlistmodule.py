# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu, \
    QTreeWidgetItemIterator, QDialog, QGridLayout

from PyQt5.QtCore import pyqtSlot, QDate, QPoint

from product.controllers.productcontroller import ProductController
from workshop.controllers.workshopcontroller import WorkshopController
from labrecord.controllers.labrecordscontroller import LabrecordsController

from workshop.modules.productputinnotemodule import ProductputinModule
from lib.sign.signmodule import SignModule

from warehouse.views.productputinlist import Ui_Form

import datetime

import user


class ProductputinlistModule(QWidget, Ui_Form):
    """ 成品寄库/入库列表记录记录
    分3个标签，0：未寄库，1：未入库，2：已入库
    点击其中一条生产记录时显示对应的记录内容
    """

    def __init__(self, parent=None):
        super(ProductputinlistModule, self).__init__(parent)
        self.setupUi(self)
        self.PC = ProductController()
        self.WC = WorkshopController()
        self.LC = LabrecordsController()
        # 获取当前状态的批生产记录
        self.get_proddetail()

    def get_proddetail(self):
        self.treeWidget_prodlist.clear()
        # self.treeWidget_prodlist.hideColumn(0)
        values_tuple_prod = (
            "autoid", "prodid", "prodname", "commonname", "spec", "package",
            "realamount", "basicunit"
        )
        key_dict_prod = dict()

        values_list_putin = ('ppid',)
        index = self.tabWidget.currentIndex()
        key_dict_putin = {
            'pistatus': index + 1
        }

        id_list = self.WC.get_productputinnote(
            True, *values_list_putin, **key_dict_putin
        )
        if not len(id_list):
            return
        key_dict_prod['autoid__in'] = id_list.distinct()

        values_tuple_lab = ('status', 'ciid')
        key_dict_lab = {
            'ciid__in': id_list.distinct(),
            'labtype': 3
        }
        res_lab = self.LC.get_labrecord(
            False, *values_tuple_lab, **key_dict_lab
        )
        res_prod = self.PC.get_producingplan(
            False, *values_tuple_prod, **key_dict_prod
        )
        for item in res_prod:
            qtreeitem = QTreeWidgetItem(self.treeWidget_prodlist)
            qtreeitem.setText(0, str(item['autoid']))
            for lab_item in res_lab:
                if lab_item['ciid'] == item['autoid']:
                    qtreeitem.setText(1, CHECK_STATUS[lab_item['status']])
                    break
            qtreeitem.setText(2, item['prodid'] + ' ' + item['prodname'])
            qtreeitem.setText(3, item['commonname'])
            qtreeitem.setText(4, item['spec'])
            qtreeitem.setText(5, item['package'])
            qtreeitem.setText(6,
                              str(item['realamount']) + item['basicunit'])


        for i in range(1, 7):
            self.treeWidget_prodlist.resizeColumnToContents(i)

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        getattr(self, 'tab_' + str(p_int)).setLayout(self.gridLayout_2)
        self.get_proddetail()


    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_prodlist_itemDoubleClicked(self, qtreeitem, p_int):

        ppid = int(qtreeitem.text(0))
        dialog = QDialog(self)
        layout = QGridLayout(dialog)
        dialog.setLayout(layout)
        detail = ProductputinModule(ppid=ppid, parent=dialog)
        layout.addWidget(detail)
        detail.accepted.connect(self.get_proddetail)
        detail.accepted.connect(dialog.accept)
        dialog.show()

    @pyqtSlot(QPoint)
    def on_treeWidget_oddmentlist_customContextMenuRequested(self, pos):
        index = self.tabWidget.currentIndex()
        if index not in (1, 3, 5):
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
        if index in (1, 5):
            button1 = menu.addAction("提交寄库")
        elif index == 3:
            button2 = menu.addAction("取消寄库")

        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)

        if index in (1, 5):
            if action == button1:
                detail = {
                    'flag': 2,
                    'qaid': user.user_id,
                    'qaname': user.user_name,
                    'qadate': user.now_date
                }
                self.PC.update_oddmentdrawnotes(id_list, **detail)

                self.get_proddetail()
                self.get_oddmentdetail()

        elif index == 3:
            if action == button2:
                detail = {
                    'flag': 0,
                    'qaid': '',
                    'qaname': '',
                    'qadate': None
                }
                self.PC.update_oddmentdrawnotes(id_list, **detail)

                self.get_proddetail()
                self.get_oddmentdetail()

CHECK_STATUS = ("待请验", "待取样", "检验中", "检验合格", "检验不合格")