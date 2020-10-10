# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'labsamplelist.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(786, 587)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.refreshButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.refreshButton.sizePolicy().hasHeightForWidth())
        self.refreshButton.setSizePolicy(sizePolicy)
        self.refreshButton.setStyleSheet("")
        self.refreshButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refreshButton.setIcon(icon)
        self.refreshButton.setIconSize(QtCore.QSize(30, 30))
        self.refreshButton.setObjectName("refreshButton")
        self.horizontalLayout.addWidget(self.refreshButton)
        self.queryButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queryButton.sizePolicy().hasHeightForWidth())
        self.queryButton.setSizePolicy(sizePolicy)
        self.queryButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/logo/images/query.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.queryButton.setIcon(icon1)
        self.queryButton.setIconSize(QtCore.QSize(30, 30))
        self.queryButton.setObjectName("queryButton")
        self.horizontalLayout.addWidget(self.queryButton)
        self.recordButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.recordButton.sizePolicy().hasHeightForWidth())
        self.recordButton.setSizePolicy(sizePolicy)
        self.recordButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/logo/images/record.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.recordButton.setIcon(icon2)
        self.recordButton.setIconSize(QtCore.QSize(30, 30))
        self.recordButton.setObjectName("recordButton")
        self.horizontalLayout.addWidget(self.recordButton)
        self.printerButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printerButton.sizePolicy().hasHeightForWidth())
        self.printerButton.setSizePolicy(sizePolicy)
        self.printerButton.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/logo/images/printer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printerButton.setIcon(icon3)
        self.printerButton.setIconSize(QtCore.QSize(30, 30))
        self.printerButton.setObjectName("printerButton")
        self.horizontalLayout.addWidget(self.printerButton)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)
        self.countlabel = QtWidgets.QLabel(Form)
        self.countlabel.setObjectName("countlabel")
        self.gridLayout.addWidget(self.countlabel, 4, 0, 1, 1)
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget_labrecords = QtWidgets.QTreeWidget(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(12)
        sizePolicy.setVerticalStretch(15)
        sizePolicy.setHeightForWidth(self.treeWidget_labrecords.sizePolicy().hasHeightForWidth())
        self.treeWidget_labrecords.setSizePolicy(sizePolicy)
        self.treeWidget_labrecords.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_labrecords.setObjectName("treeWidget_labrecords")
        self.gridLayout_2.addWidget(self.treeWidget_labrecords, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.tabWidget.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.tabWidget.addTab(self.tab_6, "")
        self.tab_7 = QtWidgets.QWidget()
        self.tab_7.setObjectName("tab_7")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.tab_7)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.tabWidget.addTab(self.tab_7, "")
        self.tab_8 = QtWidgets.QWidget()
        self.tab_8.setObjectName("tab_8")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.tab_8)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.tabWidget.addTab(self.tab_8, "")
        self.tab_9 = QtWidgets.QWidget()
        self.tab_9.setObjectName("tab_9")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.tab_9)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.tabWidget.addTab(self.tab_9, "")
        self.tab_10 = QtWidgets.QWidget()
        self.tab_10.setObjectName("tab_10")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.tab_10)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.tabWidget.addTab(self.tab_10, "")
        self.tab_11 = QtWidgets.QWidget()
        self.tab_11.setObjectName("tab_11")
        self.gridLayout_12 = QtWidgets.QGridLayout(self.tab_11)
        self.gridLayout_12.setObjectName("gridLayout_12")
        self.tabWidget.addTab(self.tab_11, "")
        self.gridLayout.addWidget(self.tabWidget, 3, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.refreshButton.setToolTip(_translate("Form", "<html><head/><body><p>刷新</p></body></html>"))
        self.queryButton.setToolTip(_translate("Form", "<html><head/><body><p>查询记录</p></body></html>"))
        self.recordButton.setToolTip(_translate("Form", "<html><head/><body><p>查看记录</p></body></html>"))
        self.printerButton.setToolTip(_translate("Form", "<html><head/><body><p>打印</p></body></html>"))
        self.countlabel.setText(_translate("Form", "共0条记录"))
        self.treeWidget_labrecords.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_labrecords.headerItem().setText(1, _translate("Form", "编号"))
        self.treeWidget_labrecords.headerItem().setText(2, _translate("Form", "名称"))
        self.treeWidget_labrecords.headerItem().setText(3, _translate("Form", "含量规格"))
        self.treeWidget_labrecords.headerItem().setText(4, _translate("Form", "包装规格"))
        self.treeWidget_labrecords.headerItem().setText(5, _translate("Form", "进程批号"))
        self.treeWidget_labrecords.headerItem().setText(6, _translate("Form", "厂家批号"))
        self.treeWidget_labrecords.headerItem().setText(7, _translate("Form", "检品数量"))
        self.treeWidget_labrecords.headerItem().setText(8, _translate("Form", "样品数量"))
        self.treeWidget_labrecords.headerItem().setText(9, _translate("Form", "样品来源"))
        self.treeWidget_labrecords.headerItem().setText(10, _translate("Form", "请验时间"))
        self.treeWidget_labrecords.headerItem().setText(11, _translate("Form", "请验人"))
        self.treeWidget_labrecords.headerItem().setText(12, _translate("Form", "请验备注"))
        self.treeWidget_labrecords.headerItem().setText(13, _translate("Form", "取样时间"))
        self.treeWidget_labrecords.headerItem().setText(14, _translate("Form", "取样人"))
        self.treeWidget_labrecords.headerItem().setText(15, _translate("Form", "取样备注"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Form", "入库物料"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "库存物料"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "前处理物料"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "半成品"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Form", "成品"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_6), _translate("Form", "退货"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_7), _translate("Form", "留样"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_8), _translate("Form", "注射用水"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_9), _translate("Form", "纯化水"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_10), _translate("Form", "环境监测"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_11), _translate("Form", "验证"))
import stuffimages_rc