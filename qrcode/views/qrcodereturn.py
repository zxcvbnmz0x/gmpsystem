# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qrcodereturn.ui'
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
        self.treeWidget_orderlist = QtWidgets.QTreeWidget(self.tab_0)
        self.treeWidget_orderlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_orderlist.setObjectName("treeWidget_orderlist")
        self.gridLayout_2.addWidget(self.treeWidget_orderlist, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_0, "")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget_orderlist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_orderlist.headerItem().setText(1, _translate("Form", "建立日期"))
        self.treeWidget_orderlist.headerItem().setText(2, _translate("Form", "退货原因"))
        self.treeWidget_orderlist.headerItem().setText(3, _translate("Form", "退货日期"))
        self.treeWidget_orderlist.headerItem().setText(4, _translate("Form", "客户"))
        self.treeWidget_orderlist.headerItem().setText(5, _translate("Form", "生产日期"))
        self.treeWidget_orderlist.headerItem().setText(6, _translate("Form", "审核人"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), _translate("Form", "未生成"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Form", "已生成"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "全部"))