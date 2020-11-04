# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDate

from equipment.controllers.equipmentcontroller import EquipmentController
from equipment.views.maintenance import Ui_Dialog

import user


class MaintenanceModule(QDialog, Ui_Dialog):
    def __init__(self, autoid=None, eqno=None, parent=None):
        super(MaintenanceModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        self.eqno = eqno
        self.ori_detail = dict()
        self.new_detail = dict()
        self.EC = EquipmentController()
        self.get_detail()

    def get_detail(self):
        if self.autoid is None:
            self.dateEdit_finishdate.setDate(user.now_date)
            if self.eqno is not None:
                key_dict = {'eqno': self.eqno}
                res = self.EC.get_data(0, True, *VALUES_TUPLE_EQ, **key_dict)
                if len(res):
                    self.label_eqno.setText(self.eqno)
                    self.label_eqname.setText(res[0])
            return
        key_dict = {'autoid': self.autoid, 'kind': 1}
        res = self.EC.get_data(3, False, **key_dict).extra(
            select={'eqname': 'equipments.eqname'},
            tables=['equipments'],
            where=['equipments.eqno=eqrepairnotes.eqno']
        ).values(*VALUES_TUPLE_NOTE)
        if not len(res):
            return
        self.ori_detail = res[0]
        self.label_eqno.setText(self.ori_detail['eqno'])
        self.label_eqname.setText(self.ori_detail['eqname'])
        self.comboBox_level.setCurrentIndex(self.ori_detail['level'])
        self.plainTextEdit_mainpoint.setPlainText(self.ori_detail['mainpoint'])
        self.plainTextEdit_part.setPlainText(self.ori_detail['partreplacing'])
        self.plainTextEdit_running.setPlainText(self.ori_detail['testrunning'])
        self.pushButton_repairer.setSign(
            self.ori_detail['repairerid'] + ' ' + self.ori_detail['repairername']
        )
        self.dateEdit_finishdate.setDate(self.ori_detail['finishdate'])

    @pyqtSlot(int)
    def on_comboBox_level_currentIndexChanged(self, p_int):
        try:
            if p_int != self.ori_detail['level']:
                self.new_detail['level'] = p_int
            else:
                try:
                    del self.new_detail['level']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['level'] = p_int

    @pyqtSlot()
    def on_plainTextEdit_mainpoint_textChanged(self):
        p_str = self.plainTextEdit_mainpoint.toPlainText()
        try:
            if p_str != self.ori_detail['mainpoint']:
                self.new_detail['remark'] = p_str
            else:
                try:
                    del self.new_detail['mainpoint']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['mainpoint'] = p_str

    @pyqtSlot()
    def on_plainTextEdit_part_textChanged(self):
        p_str = self.plainTextEdit_part.toPlainText()
        try:
            if p_str != self.ori_detail['partreplacing']:
                self.new_detail['partreplacing'] = p_str
            else:
                try:
                    del self.new_detail['partreplacing']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['partreplacing'] = p_str

    @pyqtSlot()
    def on_plainTextEdit_running_textChanged(self):
        p_str = self.plainTextEdit_running.toPlainText()
        try:
            if p_str != self.ori_detail['testrunning']:
                self.new_detail['testrunning'] = p_str
            else:
                try:
                    del self.new_detail['testrunning']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['testrunning'] = p_str

    @pyqtSlot(str)
    def on_pushButton_repairer_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['repairerid'] or name != self.ori_detail[
                'repairername']:
                self.new_detail['repairerid'] = id
                self.new_detail['repairername'] = name
            else:
                try:
                    del self.new_detail['repairerid']
                    del self.new_detail['repairername']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['repairerid'] = id
            self.new_detail['repairername'] = name

    @pyqtSlot(QDate)
    def on_dateEdit_finishdate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['finishdate']) is str:
                self.new_detail['finishdate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['finishdate']):
                self.new_detail['finishdate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['finishdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['finishdate'] = q_date.toPyDate()

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if len(self.new_detail):
            if self.autoid is None:
                self.new_detail['eqno'] = self.eqno
                self.new_detail['kind'] = 1
            self.EC.update_data(3, **self.new_detail)
        self.accept()

    pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()


VALUES_TUPLE_EQ = ('eqname', )
VALUES_TUPLE_NOTE = (
    'eqno', 'eqname', 'level', 'partreplacing', 'mainpoint', 'testrunning',
    'repairerid', 'repairername', 'finishdate'
)