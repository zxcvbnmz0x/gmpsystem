# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newpurchaseregistration.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(818, 546)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_remark = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_remark.setEnabled(False)
        self.lineEdit_remark.setObjectName("lineEdit_remark")
        self.gridLayout_2.addWidget(self.lineEdit_remark, 0, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 2, 1, 1)
        self.lineEdit_purchdate = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_purchdate.setEnabled(False)
        self.lineEdit_purchdate.setObjectName("lineEdit_purchdate")
        self.gridLayout_2.addWidget(self.lineEdit_purchdate, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget_orderlist = QtWidgets.QTreeWidget(self.groupBox)
        self.treeWidget_orderlist.setObjectName("treeWidget_orderlist")
        self.gridLayout.addWidget(self.treeWidget_orderlist, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 4, 0, 1, 4)
        self.lineEdit_supplyer = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_supplyer.setEnabled(False)
        self.lineEdit_supplyer.setObjectName("lineEdit_supplyer")
        self.gridLayout_2.addWidget(self.lineEdit_supplyer, 1, 3, 1, 1)
        self.lineEdit_regno = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_regno.setObjectName("lineEdit_regno")
        self.gridLayout_2.addWidget(self.lineEdit_regno, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.lineEdit_buyer = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_buyer.setEnabled(False)
        self.lineEdit_buyer.setObjectName("lineEdit_buyer")
        self.gridLayout_2.addWidget(self.lineEdit_buyer, 2, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 2, 2, 1, 1)
        self.lineEdit_purchno = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_purchno.setEnabled(False)
        self.lineEdit_purchno.setObjectName("lineEdit_purchno")
        self.gridLayout_2.addWidget(self.lineEdit_purchno, 2, 3, 1, 1)
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
        self.gridLayout_2.addLayout(self.horizontalLayout, 3, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "新建进货登记单"))
        self.label_2.setText(_translate("Dialog", "采购日期："))
        self.label_5.setText(_translate("Dialog", "供应商："))
        self.label.setText(_translate("Dialog", "登记单号："))
        self.groupBox.setTitle(_translate("Dialog", "采购单列表"))
        self.treeWidget_orderlist.headerItem().setText(0, _translate("Dialog", "id"))
        self.treeWidget_orderlist.headerItem().setText(1, _translate("Dialog", "采购单号"))
        self.treeWidget_orderlist.headerItem().setText(2, _translate("Dialog", "采购日期"))
        self.treeWidget_orderlist.headerItem().setText(3, _translate("Dialog", "供应商"))
        self.treeWidget_orderlist.headerItem().setText(4, _translate("Dialog", "采购员"))
        self.label_4.setText(_translate("Dialog", "备注："))
        self.label_3.setText(_translate("Dialog", "采购员："))
        self.label_6.setText(_translate("Dialog", "采购单号："))
        self.pushButton_accept.setText(_translate("Dialog", "确认"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))
