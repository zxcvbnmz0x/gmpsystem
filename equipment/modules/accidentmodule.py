# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot, QDate, QDateTime

from equipment.controllers.equipmentcontroller import EquipmentController
from equipment.views.accident import Ui_Dialog

import datetime
import user


class AccidentModule(QDialog, Ui_Dialog):
    def __init__(self, autoid=None, eqno=None, parent=None):
        super(AccidentModule, self).__init__(parent)
        self.setupUi(self)
        self.autoid = autoid
        self.eqno = eqno
        self.ori_detail = dict()
        self.new_detail = dict()
        self.EC = EquipmentController()
        self.get_detail()

    def get_detail(self):
        if self.autoid is None:
            self.dateTimeEdit_occurdate.setDateTime(user.time)
            self.dateEdit_filldate.setDate(user.now_date)
            if self.eqno is not None:
                key_dict = {'eqno': self.eqno}
                res = self.EC.get_data(0, True, *VALUES_TUPLE_EQ, **key_dict)
                if len(res):
                    self.label_eqno.setText(self.eqno)
                    self.label_eqname.setText(res[0])
            return
        key_dict = {'autoid': self.autoid}
        res = self.EC.get_data(4, False, **key_dict).extra(
            select={'eqname': 'equipments.eqname'},
            tables=['equipments'],
            where=['equipments.eqno=eqaccidentnotes.eqno']
        ).values(*VALUES_TUPLE_NOTE)
        if not len(res):
            return
        self.ori_detail = res[0]
        self.label_eqno.setText(self.ori_detail['eqno'])
        self.label_eqname.setText(self.ori_detail['eqname'])
        self.lineEdit_place.setText(self.ori_detail['place'])
        self.dateTimeEdit_occurdate.setDateTime(self.ori_detail['occurdate'])
        self.lineEdit_factormen.setText(self.ori_detail['factormen'])
        self.lineEdit_kind.setText(self.ori_detail['kind'])
        self.lineEdit_injury.setText(self.ori_detail['injury'])
        self.plainTextEdit_brief.setPlainText(self.ori_detail['brief'])
        self.plainTextEdit_reason.setPlainText(self.ori_detail['reason'])
        self.plainTextEdit_loss.setPlainText(self.ori_detail['loss'])
        self.plainTextEdit_treatadvice.setPlainText(self.ori_detail['treatadvice'])
        self.plainTextEdit_chargeradvice.setPlainText(
            self.ori_detail['chargeradvice']
        )
        self.pushButton_filler.setSign(
            self.ori_detail['fillerid'] + ' ' + self.ori_detail['fillername']
        )
        self.dateEdit_filldate.setDate(self.ori_detail['filldate'])

    @pyqtSlot(str)
    def on_lineEdit_place_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['place']:
                self.new_detail['place'] = p_str
            else:
                try:
                    del self.new_detail['place']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['place'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_factormen_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['factormen']:
                self.new_detail['factormen'] = p_str
            else:
                try:
                    del self.new_detail['factormen']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['factormen'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_kind_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['kind']:
                self.new_detail['kind'] = p_str
            else:
                try:
                    del self.new_detail['kind']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['kind'] = p_str

    @pyqtSlot(str)
    def on_lineEdit_injury_textChanged(self, p_str):
        try:
            if p_str != self.ori_detail['injury']:
                self.new_detail['injury'] = p_str
            else:
                try:
                    del self.new_detail['injury']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['injury'] = p_str

    @pyqtSlot()
    def on_plainTextEdit_brief_textChanged(self):
        p_str = self.plainTextEdit_brief.toPlainText()
        try:
            if p_str != self.ori_detail['brief']:
                self.new_detail['brief'] = p_str
            else:
                try:
                    del self.new_detail['brief']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['brief'] = p_str

    @pyqtSlot()
    def on_plainTextEdit_reason_textChanged(self):
        p_str = self.plainTextEdit_reason.toPlainText()
        try:
            if p_str != self.ori_detail['reason']:
                self.new_detail['reason'] = p_str
            else:
                try:
                    del self.new_detail['reason']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['reason'] = p_str

    @pyqtSlot()
    def on_plainTextEdit_loss_textChanged(self):
        p_str = self.plainTextEdit_loss.toPlainText()
        try:
            if p_str != self.ori_detail['loss']:
                self.new_detail['loss'] = p_str
            else:
                try:
                    del self.new_detail['loss']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['loss'] = p_str

    @pyqtSlot()
    def on_plainTextEdit_treatadvice_textChanged(self):
        p_str = self.plainTextEdit_loss.toPlainText()
        try:
            if p_str != self.ori_detail['treatadvice']:
                self.new_detail['treatadvice'] = p_str
            else:
                try:
                    del self.new_detail['treatadvice']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['treatadvice'] = p_str

    @pyqtSlot()
    def on_plainTextEdit_chargeradvice_textChanged(self):
        p_str = self.plainTextEdit_loss.toPlainText()
        try:
            if p_str != self.ori_detail['chargeradvice']:
                self.new_detail['chargeradvice'] = p_str
            else:
                try:
                    del self.new_detail['chargeradvice']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['chargeradvice'] = p_str

    @pyqtSlot(str)
    def on_pushButton_filler_signChanged(self, p_str):
        if len(p_str.split(' ')) != 2 and p_str != '':
            return
        id, name = p_str.split(' ') if p_str != '' else ('', '')
        try:
            if id != self.ori_detail['fillerid'] or name != self.ori_detail[
                'fillername']:
                self.new_detail['fillerid'] = id
                self.new_detail['fillername'] = name
            else:
                try:
                    del self.new_detail['fillerid']
                    del self.new_detail['fillername']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['fillerid'] = id
            self.new_detail['fillername'] = name

    @pyqtSlot(QDate)
    def on_dateEdit_filldate_dateChanged(self, q_date):
        try:
            if type(self.ori_detail['filldate']) is str:
                self.new_detail['filldate'] = q_date.toPyDate()
                return
            if q_date != QDate(self.ori_detail['filldate']):
                self.new_detail['filldate'] = q_date.toPyDate()
            else:
                try:
                    del self.new_detail['filldate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['filldate'] = q_date.toPyDate()

    @pyqtSlot(QDateTime)
    def on_dateTimeEdit_occurdate_dateTimeChanged(self, q_time):
        if not q_time.isValid():
            return
        qdtime = q_time.toPyDateTime().strftime('%Y-%m-%d %H:%M')
        try:
            if qdtime != self.ori_detail['occurdate'].\
                    strftime('%Y-%m-%d %H:%M'):
                self.new_detail['occurdate'] = qdtime
            else:
                try:
                    del self.new_detail['occurdate']
                except KeyError:
                    pass
        except KeyError:
            self.new_detail['occurdate'] = qdtime


    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        condition = dict()
        if len(self.new_detail):
            if self.autoid is None:
                self.new_detail['eqno'] = self.eqno
            else:
                condition['autoid'] = self.autoid
            self.EC.update_data(4, condition, **self.new_detail)
        self.accept()

    pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()


VALUES_TUPLE_EQ = ('eqname', )
VALUES_TUPLE_NOTE = (
    'eqno', 'eqname', 'place', 'occurdate', 'factormen', 'kind', 'injury',
    'brief', 'reason', 'loss', 'treatadvice', 'chargeradvice', 'fillerid',
    'fillername', 'filldate'
)