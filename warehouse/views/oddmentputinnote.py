# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'oddmentputinnote.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(785, 583)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_0 = QtWidgets.QWidget()
        self.tab_0.setObjectName("tab_0")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget_prodlist = QtWidgets.QTreeWidget(self.tab_0)
        self.treeWidget_prodlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_prodlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_prodlist.setObjectName("treeWidget_prodlist")
        self.gridLayout_2.addWidget(self.treeWidget_prodlist, 0, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab_0)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.treeWidget_oddmentlist = QtWidgets.QTreeWidget(self.groupBox)
        self.treeWidget_oddmentlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_oddmentlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_oddmentlist.setObjectName("treeWidget_oddmentlist")
        self.gridLayout_3.addWidget(self.treeWidget_oddmentlist, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_0, "")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tabWidget.addTab(self.tab_1, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget_prodlist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_prodlist.headerItem().setText(1, _translate("Form", "产品名称"))
        self.treeWidget_prodlist.headerItem().setText(2, _translate("Form", "通用名"))
        self.treeWidget_prodlist.headerItem().setText(3, _translate("Form", "含量规格"))
        self.treeWidget_prodlist.headerItem().setText(4, _translate("Form", "包装规格"))
        self.treeWidget_prodlist.headerItem().setText(5, _translate("Form", "计划产量"))
        self.groupBox.setTitle(_translate("Form", "登记项目"))
        self.treeWidget_oddmentlist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_oddmentlist.headerItem().setText(1, _translate("Form", "数量"))
        self.treeWidget_oddmentlist.headerItem().setText(2, _translate("Form", "单位"))
        self.treeWidget_oddmentlist.headerItem().setText(3, _translate("Form", "登记人"))
        self.treeWidget_oddmentlist.headerItem().setText(4, _translate("Form", "登记日期"))
        self.treeWidget_oddmentlist.headerItem().setText(5, _translate("Form", "过期日期"))
        self.treeWidget_oddmentlist.headerItem().setText(6, _translate("Form", "寄库人"))
        self.treeWidget_oddmentlist.headerItem().setText(7, _translate("Form", "寄库日期"))
        self.treeWidget_oddmentlist.headerItem().setText(8, _translate("Form", "接收人"))
        self.treeWidget_oddmentlist.headerItem().setText(9, _translate("Form", "接收日期"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), _translate("Form", "已寄库"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Form", "已入库"))
