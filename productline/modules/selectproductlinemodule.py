# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

from productline.controllers.productlineconroller import ProductLineConroller
from productline.views.selectproductline import Ui_Dialog


class SelectProductLine(QtWidgets.QDialog, Ui_Dialog):
    select_line_signal = QtCore.pyqtSignal(dict)

    def __init__(self, parent=None, pltype=None):
        super().__init__(parent)
        self.setupUi(self)
        self.plcontroller = ProductLineConroller()
        res = self.plcontroller.get_productline(pltype=pltype)
        self.set_data(res)

    def set_data(self, items):
        try:
            for item in items:
                treeitem = QtWidgets.QTreeWidgetItem(self.productlinelist)
                treeitem.setText(0, str(item.autoid))
                treeitem.setText(1, item.linename)
                treeitem.setText(2, item.deptid)
                treeitem.setText(3, item.deptname)
            self.productlinelist.hideColumn(0)
            for i in range(1, 5):
                self.productlinelist.resizeColumnToContents(i)
            self.countlabel.setText("共%s条记录" % len(items))
        except Exception as e:
            print(repr(e))

    # 双击生产线就直接选择该生产线
    @QtCore.pyqtSlot(QtWidgets.QTreeWidgetItem, int)
    def on_productlinelist_itemDoubleClicked(self, qtreeitem, p_int):
        self.on_acceptButton_clicked()

    # 确认功能
    @QtCore.pyqtSlot()
    def on_acceptButton_clicked(self):
        selectitem = dict()
        # 当前选择项目的autoid
        selectitem['autoid'] = self.productlinelist.currentItem().text(0)
        selectitem['linename'] = self.productlinelist.currentItem().text(1)
        selectitem['deptname'] = self.productlinelist.currentItem().text(3)
        if selectitem:
            self.select_line_signal.emit(selectitem)
            self.accept()

    # 取消功能
    @QtCore.pyqtSlot()
    def on_cancelButton_clicked(self):
        self.close()