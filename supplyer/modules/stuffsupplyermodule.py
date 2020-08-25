# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtGui, QtWidgets

from supplyer.models.supplyermodel import SupplyerModel

from supplyer.views.spandpd import Ui_Dialog


class StuffSupplyerModule(QtWidgets.QDialog, Ui_Dialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        # 修改前数据，若为新建则为空
        self.oridetail = dict()
        # 修改后的数据，自动把修改过的数据添加到字典中，
        # 若恢复原来的数据或者删除，则字典中也删除
        self.detail = dict()
        # 物料字典中的autoid，由生成界面时传入
        self.sdid: int
        # 物料供应商的autoid,仅修改记录时才有值传入
        self.autoid = 0
        # 数据库操作类
        self.supplyer_model = SupplyerModel()

    @QtCore.pyqtSlot(str)
    def on_supplyerid_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['supid']:
                self.detail['supid'] = p_str
            else:
                try:
                    del self.detail['supid']
                except KeyError:
                    pass
        except KeyError:
            self.detail['supid'] = p_str

    @QtCore.pyqtSlot(str)
    def on_supplyername_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['supname']:
                self.detail['supname'] = p_str
            else:
                try:
                    del self.detail['supname']
                except KeyError:
                    pass
        except KeyError:
            self.detail['supname'] = p_str

    @QtCore.pyqtSlot(str)
    def on_producer_textChanged(self, p_str):
        try:
            if p_str != self.oridetail['producer']:
                self.detail['producer'] = p_str
            else:
                try:
                    del self.detail['producer']
                except KeyError:
                    pass
        except KeyError:
            self.detail['producer'] = p_str

    # 确认
    @QtCore.pyqtSlot()
    def on_acceptbutton_clicked(self):
        # 有修改过数据
        try:
            # autoid不为空，则为修改记录
            # 否则为插入记录
            if self.autoid:
                res = self.supplyer_model.update_stuff_supplyer_item(
                    self.autoid,
                    **self.detail)
                if res == 1:
                    self.flush_signal.emit()
                    self.accept()
            else:
                # 把sdid加到更新内容里
                if self.sdid:
                    self.detail['sdid_id'] = int(self.sdid)
                    res = self.supplyer_model.update_stuff_supplyer_item(
                        **self.detail)
                    if res:
                        self.flush_signal.emit()
                        self.accept()
        except Exception as e:
            print(repr(e))

    # 取消
    @QtCore.pyqtSlot()
    def on_cancelbutton_clicked(self):
        self.close()
