# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qrcoderepository.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(896, 616)
        Form.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget_qrcode = QtWidgets.QTreeWidget(Form)
        self.treeWidget_qrcode.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_qrcode.setObjectName("treeWidget_qrcode")
        self.gridLayout.addWidget(self.treeWidget_qrcode, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget_qrcode.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_qrcode.headerItem().setText(1, _translate("Form", "二维码"))
        self.treeWidget_qrcode.headerItem().setText(2, _translate("Form", "产品通用名"))
        self.treeWidget_qrcode.headerItem().setText(3, _translate("Form", "批准文号"))
        self.treeWidget_qrcode.headerItem().setText(4, _translate("Form", "公司名"))
        self.treeWidget_qrcode.headerItem().setText(5, _translate("Form", "电话"))
        self.treeWidget_qrcode.headerItem().setText(6, _translate("Form", "上传时间"))
        self.treeWidget_qrcode.headerItem().setText(7, _translate("Form", "使用时间"))
        self.treeWidget_qrcode.headerItem().setText(8, _translate("Form", "状态"))
