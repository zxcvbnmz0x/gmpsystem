# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectoddmentdraw.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 300)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_accept = QtWidgets.QPushButton(Dialog)
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.horizontalLayout.addWidget(self.pushButton_accept)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.treeWidget_oddmentdrawlist = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget_oddmentdrawlist.setObjectName("treeWidget_oddmentdrawlist")
        self.gridLayout.addWidget(self.treeWidget_oddmentdrawlist, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "选择零头领取"))
        self.pushButton_accept.setText(_translate("Dialog", "确认"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))
        self.treeWidget_oddmentdrawlist.headerItem().setText(0, _translate("Dialog", "id"))
        self.treeWidget_oddmentdrawlist.headerItem().setText(1, _translate("Dialog", "批号"))
        self.treeWidget_oddmentdrawlist.headerItem().setText(2, _translate("Dialog", "数量"))
        self.treeWidget_oddmentdrawlist.headerItem().setText(3, _translate("Dialog", "单位"))
        self.treeWidget_oddmentdrawlist.headerItem().setText(4, _translate("Dialog", "登记人"))
        self.treeWidget_oddmentdrawlist.headerItem().setText(5, _translate("Dialog", "登记日期"))
        self.treeWidget_oddmentdrawlist.headerItem().setText(6, _translate("Dialog", "过期日期"))
