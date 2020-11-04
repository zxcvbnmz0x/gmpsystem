# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QWidget, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from equipment.views.eqgeneralrecordslist import Ui_Form
from equipment.controllers.equipmentcontroller import EquipmentController
from selfdefinedfirmat.controllers.selfdefinedformatcontroller import SelfdefinedformatController
from equipment.modules.selectgeneralrecors import SelectGeneralRecordsModule
from equipment.modules.generalrecordmodule import GeneralRecordModule

import datetime
import user


class EqGeneralRecorsListModule(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(EqGeneralRecorsListModule, self).__init__(parent)
        self.setupUi(self)
        self.EC = EquipmentController()
        self.SC = SelfdefinedformatController()
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

    def get_generalrecors_note(self):
        self.treeWidget_recordslist.clear()
        index = self.tabWidget.currentIndex()
        key_dict = {
            'eqno': self.eqno,
            'status': index,
        }
        res = self.EC.get_data(5, False, *VALUES_TUPLE_RECORDS, **key_dict)
        if not len(res):
            return
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_recordslist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, item['formname'])
            qtreeitem.setText(
                2, item['createtime'].strftime('%Y-%m-%d %H:%M') if type(
                    item['createtime']) is datetime.datetime else ''
            )
            qtreeitem.setText(3, item['creatorid'] + ' ' + item['creatorname'])
        for i in range(1, 4):
            self.treeWidget_recordslist.resizeColumnToContents(i)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equuiplist_itemDoubleClicked(self, qtreeitem, p_int):
        self.eqno = qtreeitem.text(1)
        self.get_generalrecors_note()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_deptlist_itemDoubleClicked(self, qtreeitem, p_int):
        self.deptid = qtreeitem.text(1)
        self.get_eq_detail()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_equiplist_itemDoubleClicked(self, qtreeitem, p_int):
        self.eqid = qtreeitem.text(0)
        self.get_generalrecors_note()

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
        self.get_generalrecors_note()

    @pyqtSlot(QPoint)
    def on_treeWidget_recordslist_customContextMenuRequested(self, pos):
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        index = self.tabWidget.currentIndex()
        menu = QMenu()
        button1 = menu.addAction("增加一般记录")
        button2 = menu.addAction("修改一般记录")
        button3 = menu.addAction("删除一般记录")
        menu.addSeparator()
        button4 = menu.addAction("提交完成")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if action == button1:
            if self.eqno != '':
                detail = SelectGeneralRecordsModule(self)
                detail.accepted.connect(self.get_generalrecors_note)
                detail.selected.connect(self.new_general_records)
                detail.show()
        elif action == button2:
            if current_item is not None and index == 0:
                id = int(current_item.text(0))
                detail = GeneralRecordModule(id, self)
                detail.accepted.connect(self.get_generalrecors_note)
                detail.show()
        elif action == button3:
            if current_item is not None:
                id = int(current_item.text(0))
                condition = {'autoid': id}
                self.EC.delete_data(5, condition)
                self.get_generalrecors_note()
        elif action == button4:
            if current_item is not None and index == 0:
                id = int(current_item.text(0))
                condition = {'autoid': id}
                kwargs = {'status': 1}
                self.EC.update_data(5, condition, **kwargs)
                self.get_generalrecors_note()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_recordslist_itemDoubleClicked(self, qtreeitem, p_int):
        id = int(qtreeitem.text(0))
        detail = GeneralRecordModule(id, self)
        detail.accepted.connect(self.get_generalrecors_note)
        detail.show()

    def new_general_records(self, id_tuple):
        if len(id_tuple) == 0:
            return
        else:
            key_dict = dict()
            key_dict['autoid__in'] = id_tuple
            res = self.SC.get_selfdefinedformat(
                False, *VALUES_TUPLE_SD, **key_dict
            )
            for item in res:
                kwargs = {
                    'eqno': self.eqno,
                    'creatorid': user.user_id,
                    'creatorname': user.user_name,
                    'formname': item['formatname'],
                    'kind': item['kind'],
                    'subkind': item['subkind'],
                    'format': item['format'],
                    'createtime': user.now_time
                }
                self.EC.update_data(5, **kwargs)



VALUES_TUPLE_EQ = ('autoid', 'eqno', 'eqname', 'instposition')
VALUES_TUPLE_DP = ('deptid', 'deptname')
VALUES_TUPLE_RECORDS = (
    'autoid', 'formname',  'creatorid', 'creatorname', 'createtime'
)
VALUES_TUPLE_SD =('formatname', 'subkind', 'kind', 'format')