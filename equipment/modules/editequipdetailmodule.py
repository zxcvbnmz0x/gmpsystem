# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QMenu
from PyQt5.QtCore import pyqtSlot, QPoint

from equipment.views.editequipdetail import Ui_Dialog
from equipment.controllers.equipmentcontroller import EquipmentController
from equipment.modules.editeqcheckdetailmodule import EditEquCheckDetailModule

from lib.utils.messagebox import MessageBox


class EditEquipDetailModule(QDialog, Ui_Dialog):
    def __init__(self, autoid=None, parent=None):
        super(EditEquipDetailModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        self.EC = EquipmentController()
        self.ori_detail = dict()
        self.new_detail = dict()

        self.lineEdit_dept.setup(
            'Department', RETURN_ROW_DEPT, CONDITION_KEY_DEPT,
            TREEHEADER_NAME_DEPT, 350, 190
        )
        self.lineEdit_maintainer.setup(
            'Clerks', RETURN_ROW_MAINTAINER, CONDITION_KEY_MAINTAINER,
            TREEHEADER_NAME_MAINTAINER, 350,190
        )
        self.get_detail()
        self.get_check_detail()

    def get_detail(self):
        if self.autoid is None:
            return
        key_dict = {'autoid': self.autoid}
        res = self.EC.get_data(0, False, *VALUES_TUPLE_EQ, **key_dict)
        if not len(res):
            return
        self.ori_detail = res[0]
        self.lineEdit_id.setText(self.ori_detail['eqno'])
        self.lineEdit_name.setText(self.ori_detail['eqname'])
        self.lineEdit_NO.setText(self.ori_detail['serialno'])
        self.lineEdit_spec.setText(self.ori_detail['spec'])
        self.lineEdit_price.setText(self.ori_detail['price'])
        self.lineEdit_producer.setText(self.ori_detail['manufacturer'])
        self.lineEdit_makedate.setText(self.ori_detail['makedate'])
        self.lineEdit_indate.setText(self.ori_detail['indate'])
        self.comboBox_type.setCurrentIndex(self.ori_detail['eqtype'])
        self.lineEdit_location.setText(self.ori_detail['instposition'])
        self.lineEdit_parameter.setText(self.ori_detail['parameter'])
        self.lineEdit_performance.setText(self.ori_detail['performance'])
        self.lineEdit_dept.setText(
            self.ori_detail['deptid'] + ' ' + self.ori_detail['deptname']
        )
        self.lineEdit_maintainer.setText(
            self.ori_detail['maintainerid'] + ' ' + \
            self.ori_detail['maintainername']
        )
        self.lineEdit_remark.setText(self.ori_detail['remark'])
        self.comboBox_status.setCurrentIndex(self.ori_detail['status'])

    def get_check_detail(self):
        self.treeWidget_checklist.clear()
        # self.treeWidget_checklist.hideColumn(0)
        if self.autoid is None:
            return
        key_dict = {'eqid': self.autoid}
        res = self.EC.get_data(2, False, *VALUES_TUPLE_EQCHECK, **key_dict)
        for item in res:
            qtreeitem = QTreeWidgetItem(self.treeWidget_checklist)
            qtreeitem.setText(0, str(item['autoid']))
            qtreeitem.setText(1, STAUTS[item['status']])
            qtreeitem.setText(2, str(item['checkdate']))
            qtreeitem.setText(3, item['company'])
            qtreeitem.setText(4, item['result'])
            qtreeitem.setText(
                5, item['registerid'] + ' ' + item['registername']
            )
        for i in range(1, 6):
            self.treeWidget_checklist.resizeColumnToContents(i)


    @pyqtSlot(str)
    def on_lineEdit_id_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['eqno']:
                self.new_detail['eqno'] = p_str
            else:
                try:
                    del self.new_detail['eqno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['eqno'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_name_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['eqname']:
                self.new_detail['eqname'] = p_str
            else:
                try:
                    del self.new_detail['eqname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['eqname'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_NO_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['serialno']:
                self.new_detail['serialno'] = p_str
            else:
                try:
                    del self.new_detail['serialno']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['serialno'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_spec_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['spec']:
                self.new_detail['spec'] = p_str
            else:
                try:
                    del self.new_detail['spec']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['spec'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_price_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['price']:
                self.new_detail['price'] = p_str
            else:
                try:
                    del self.new_detail['price']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['price'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_producer_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['manufacturer']:
                self.new_detail['manufacturer'] = p_str
            else:
                try:
                    del self.new_detail['manufacturer']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['manufacturer'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_makedate_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['makedate']:
                self.new_detail['makedate'] = p_str
            else:
                try:
                    del self.new_detail['makedate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['makedate'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_indate_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['indate']:
                self.new_detail['indate'] = p_str
            else:
                try:
                    del self.new_detail['indate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['indate'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_location_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['instposition']:
                self.new_detail['instposition'] = p_str
            else:
                try:
                    del self.new_detail['instposition']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['instposition'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_parameter_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['parameter']:
                self.new_detail['parameter'] = p_str
            else:
                try:
                    del self.new_detail['parameter']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['parameter'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_performance_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['performance']:
                self.new_detail['performance'] = p_str
            else:
                try:
                    del self.new_detail['performance']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['performance'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_dept_textChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['deptid'] or name != self.ori_detail[
                'deptname']:
                self.new_detail['deptid'] = id
                self.new_detail['deptname'] = name
            else:
                try:
                    del self.new_detail['deptid']
                    del self.new_detail['deptname']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['deptid'] = id
            self.new_detail['deptname'] = name

    @pyqtSlot(str)
    def on_lineEdit_maintainer_textChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['maintainerid'] or name != self.ori_detail[
                'maintainername']:
                self.new_detail['maintainerid'] = id
                self.new_detail['maintainername'] = name
            else:
                try:
                    del self.new_detail['maintainerid']
                    del self.new_detail['maintainername']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['maintainerid'] = id
            self.new_detail['maintainername'] = name

    @pyqtSlot(str)
    def on_lineEdit_remark_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['remark']:
                self.new_detail['remark'] = p_str
            else:
                try:
                    del self.new_detail['remark']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['remark'] = p_str

    @pyqtSlot(int)
    def on_comboBox_type_currentIndexChanged(self, p_int):
        try:
            if p_int != self.ori_detail['eqtype']:
                self.new_detail['eqtype'] = p_int
            else:
                try:
                    del self.new_detail['eqtype']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['eqtype'] = p_int

    @pyqtSlot(int)
    def on_comboBox_status_currentIndexChanged(self, p_int):
        try:
            if p_int != self.ori_detail['status']:
                self.new_detail['status'] = p_int
            else:
                try:
                    del self.new_detail['status']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['status'] = p_int

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if not self.autoid or 'eqno' in self.new_detail:
            eqno = self.lineEdit_id.text()
            key_dict = {'eqno': eqno}
            res = self.EC.get_data(0, True, 'autoid', **key_dict)
            if len(res):
                msg = MessageBox(self, text="设备编号重复")
                msg.show()
                return
        if len(self.new_detail):
            if self.autoid:
                condition = {'autoid': self.autoid}
                self.EC.update_data(0, condition, **self.new_detail)
            else:
                self.EC.update_data(0, **self.new_detail)
        self.accept()

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()


    @pyqtSlot(QPoint)
    def on_treeWidget_checklist_customContextMenuRequested(self, pos):
        sender_widget = self.sender()
        current_item = sender_widget.currentItem()
        menu = QMenu()
        button1 = menu.addAction("增加校验记录")
        button2 = menu.addAction("修改校验记录")
        button3 = menu.addAction("删除校验记录")
        menu.addSeparator()
        button4 = menu.addAction("提交完成")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        if action == button1:
            detail = EditEquCheckDetailModule(eqid=self.autoid, parent=self)
            detail.accepted.connect(self.get_check_detail)
            detail.show()
        elif action == button2:
            if current_item is None:
                return
            id = int(current_item.text(0))
            status = current_item.text(1)
            if status == "完成":
                return
            detail = EditEquCheckDetailModule(id, self.autoid, self)
            detail.accepted.connect(self.get_check_detail)
            detail.show()
        elif action == button3:
            if current_item is None:
                return
            id = int(current_item.text(0))
            print(id)
            condition = {'autoid': id}
            self.EC.delete_data(2, condition)
            self.get_check_detail()
        elif action == button4:
            if current_item is None:
                return
            id = int(current_item.text(0))
            condition = {'autoid': id}
            detail = {'status': 1}
            self.EC.update_data(2, condition, **detail)
            self.get_check_detail()

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_checklist_itemDoubleClicked(self, qtreeitem, p_int):
        id = int(qtreeitem.text(0))
        detail = EditEquCheckDetailModule(id, self.autoid, self)
        detail.accepted.connect(self.get_check_detail)
        detail.show()


RETURN_ROW_DEPT = ('autoid', 'deptid', 'deptname')
CONDITION_KEY_DEPT = ('deptid', 'deptname', 'inputcode')
TREEHEADER_NAME_DEPT = ("id", "编号", "姓名")

RETURN_ROW_MAINTAINER = ('clerkid', 'pid', 'clerkname')
CONDITION_KEY_MAINTAINER = ('pid', 'clerkname', 'inputcode')
TREEHEADER_NAME_MAINTAINER = ("id", "编号", "名称")

VALUES_TUPLE_EQ = (
    'eqno', 'eqname', 'eqtype', 'serialno', 'spec', 'price', 'manufacturer',
    'indate', 'maintainerid', 'maintainername', 'deptid', 'deptname',
    'instposition', 'makedate', 'parameter', 'performance', 'status', 'remark'
)
VALUES_TUPLE_EQCHECK = (
    'autoid', 'checkdate', 'company', 'result', 'status', 'registerid',
    'registername'
)
STAUTS = ("编辑中", "完成")