# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'midproddrawnote.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(821, 480)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.treeWidget_midproductlist = QtWidgets.QTreeWidget(Form)
        self.treeWidget_midproductlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_midproductlist.setIndentation(0)
        self.treeWidget_midproductlist.setObjectName("treeWidget_midproductlist")
        self.gridLayout.addWidget(self.treeWidget_midproductlist, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_workersign = QtWidgets.QPushButton(Form)
        self.pushButton_workersign.setObjectName("pushButton_workersign")
        self.horizontalLayout.addWidget(self.pushButton_workersign)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget_midproductlist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_midproductlist.headerItem().setText(1, _translate("Form", "瓶/袋/桶号"))
        self.treeWidget_midproductlist.headerItem().setText(2, _translate("Form", "数量"))
        self.treeWidget_midproductlist.headerItem().setText(3, _translate("Form", "登记人"))
        self.treeWidget_midproductlist.headerItem().setText(4, _translate("Form", "日期"))
        self.treeWidget_midproductlist.headerItem().setText(5, _translate("Form", "工人"))
        self.pushButton_workersign.setText(_translate("Form", "工人签名"))
