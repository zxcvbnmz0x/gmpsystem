# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oddmentdrawnote.ui'
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
        self.treeWidget_oddmentlist = QtWidgets.QTreeWidget(Form)
        self.treeWidget_oddmentlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_oddmentlist.setIndentation(0)
        self.treeWidget_oddmentlist.setObjectName("treeWidget_oddmentlist")
        self.gridLayout.addWidget(self.treeWidget_oddmentlist, 0, 0, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget_oddmentlist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_oddmentlist.headerItem().setText(1, _translate("Form", "登记人"))
        self.treeWidget_oddmentlist.headerItem().setText(2, _translate("Form", "登记日期"))
        self.treeWidget_oddmentlist.headerItem().setText(3, _translate("Form", "登记数量"))
        self.treeWidget_oddmentlist.headerItem().setText(4, _translate("Form", "单位"))
        self.treeWidget_oddmentlist.headerItem().setText(5, _translate("Form", "批号"))
        self.treeWidget_oddmentlist.headerItem().setText(6, _translate("Form", "发放人"))
        self.treeWidget_oddmentlist.headerItem().setText(7, _translate("Form", "发放日期"))
