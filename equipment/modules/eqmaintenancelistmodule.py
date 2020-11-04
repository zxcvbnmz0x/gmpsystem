# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from equipment.views.eqmaintenancelist import Ui_Form
from equipment.controllers.equipmentcontroller import EquipmentController
from equipment.modules.maintenancemodule import MaintenanceModule

import datetime


class EqMaintenanceListModule(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(EqMaintenanceListModule, self).__init__(parent)
        self.setupUi(self)
        self.EC = EquipmentController()
        self.deptid = ''
        self.eqtype = -1
        self.eqno = ''
        self.treeWidget_equuiplist.hideColumn(0)
        self.treeWidget_deptlist.hideColumn(1)
        self.treeWidget_recordslist.hideColumn(0)
        self.get_dept_detail()
        self.get_eq_detail()

    def get_eq_detail(self):
        self.treeWidget_equuiplist.clear()
        key_dict = dict()
        if self.deptid != '':
            key_dict['deptid'] = self.deptid
        if self.eqtype != -1:
            key_dict['eqtype'] = self.eqtype

        res = self.EC.get_data(0, False, *VALUES_TUPLE_EQ, **key_dict)
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_equuiplist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['eqno'])
            qtreeitem.setText(2, item['eqname'])
            qtreeitem.setText(3, item['instposition'])
        for i in range(1, 4):
            self.treeWidget_equuiplist.resizeColumnToContents(i)

    def get_dept_detail(self):
        self.treeWidget_deptlist.clear()
        all_dept = QTreeWidgetItem(self.treeWidget_deptlist)
        all_dept.setText(0, "全部部门")
        all_dept.setText(1, "")
        self.treeWidget_deptlist.expandAll()
        res = self.EC.get_data(0, False, *VALUES_TUPLE_DP).distinct()
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(all_dept)
            qtreeitem.setText(0, item['deptname'])
            qtreeitem.setText(1, item['deptid'])
        self.treeWidget_deptlist.resizeColumnToContents(0)

    def get_maintenance_note(self):
        self.treeWidget_recordslist.clear()
        index = self.tabWidget.currentIndex()
        key_dict = {
            'eqno': self.eqno,
            'status': index,
            'kind': 1
        }
        res = self.EC.get_data(3, False, *VALUES_TUPLE_MAIN, **key_dict)
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_recordslist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(
                1, str(item['finishdate']) if type(item['finishdate']) is
                                               datetime.date else ''
            )
            qtreeitem.setText(2, item['repairerid'] + ' ' + item['repairername'])
            qtreeitem.setText(3, LEVEL[item['level']])
            qtreeitem.setText(4, item['mainpoint'])
            qtreeitem.setText(5, item['partreplacing'])
            qtreeitem.setText(6, item['testrunning'])
        for i in range(1, 7):
            self.treeWidget_recordslist.resizeColumnToContents(i)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equuiplist_itemDoubleClicked(self, qtreeitem, p_int):
        self.eqno = qtreeitem.text(1)
        self.get_maintenance_note()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_deptlist_itemDoubleClicked(self, qtreeitem, p_int):
        self.deptid = qtreeitem.text(1)
        self.get_eq_detail()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equiplist_itemDoubleClicked(self, qtreeitem, p_int):
        self.eqid = qtreeitem.text(0)
        self.get_maintenance_note()

    @pyqtSlot(int)
    def on_toolBox_currentChanged(self, p_int):
        current_tool = getattr(self, 'page_' + str(p_int))
        current_tool.setLayout(self.gridLayout_3)
        self.eqtype = p_int - 1
        self.get_eq_detail()

    @pyqtSlot(int)
    def on_tabWidget_currentChanged(self, p_int):
        current_tool = getattr(self, 'tab_' + str(p_int))
        current_tool.setLayout(self.gridLayout_2)
        self.get_maintenance_note()

    @pyqtSlot(QPoint)
    def on_treeWidget_recordslist_customContextMenuRequested(self, pos):
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        index = self.tabWidget.currentIndex()
        menu = QMenu()
        button1 = menu.addAction("增加维保记录")
        button2 = menu.addAction("修改维保记录")
        button3 = menu.addAction("删除维保记录")
        menu.addSeparator()
        button4 = menu.addAction("提交完成")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if action == button1:
            if self.eqno != '':
                detail = MaintenanceModule(eqno=self.eqno, parent=self)
                detail.accepted.connect(self.get_maintenance_note)
                detail.show()
        elif action == button2:
            if current_item is not None and index == 0:
                id = int(current_item.text(0))
                detail = MaintenanceModule(autoid=id, parent=self)
                detail.accepted.connect(self.get_maintenance_note)
                detail.show()
        elif action == button3:
            if current_item is not None:
                id = int(current_item.text(0))
                condition = {'autoid': id}
                self.EC.delete_data(3, condition)
                self.get_maintenance_note()
        elif action == button4:
            if current_item is not None and index == 0:
                id = int(current_item.text(0))
                condition = {'autoid': id}
                kwargs = {'status': 1}
                self.EC.update_data(3, condition, **kwargs)
                self.get_maintenance_note()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_recordslist_itemDoubleClicked(self, qtreeitem, p_int):
        id = int(qtreeitem.text(0))
        detail = MaintenanceModule(autoid=id, parent=self)
        detail.accepted.connect(self.get_maintenance_note)
        detail.show()


LEVEL = ("普通", "重要")

VALUES_TUPLE_EQ = ('autoid', 'eqno', 'eqname', 'instposition')
VALUES_TUPLE_DP = ('deptid', 'deptname')
VALUES_TUPLE_MAIN = (
    'autoid', 'level', 'partreplacing', 'mainpoint', 'testrunning',
    'repairerid', 'repairername', 'finishdate'
)
