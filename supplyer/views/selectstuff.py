# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectstuff.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(642, 469)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_accept = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_accept.sizePolicy().hasHeightForWidth())
        self.pushButton_accept.setSizePolicy(sizePolicy)
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.horizontalLayout.addWidget(self.pushButton_accept)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.treeWidget_stufflist = QtWidgets.QTreeWidget(Dialog)
        self.treeWidget_stufflist.setObjectName("treeWidget_stufflist")
        self.gridLayout.addWidget(self.treeWidget_stufflist, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "选择物料"))
        self.pushButton_accept.setText(_translate("Dialog", "确认"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))
        self.treeWidget_stufflist.headerItem().setText(0, _translate("Dialog", "id"))
        self.treeWidget_stufflist.headerItem().setText(1, _translate("Dialog", "编号"))
        self.treeWidget_stufflist.headerItem().setText(2, _translate("Dialog", "名称"))
        self.treeWidget_stufflist.headerItem().setText(3, _translate("Dialog", "含量规格"))
        self.treeWidget_stufflist.headerItem().setText(4, _translate("Dialog", "包装规格"))
