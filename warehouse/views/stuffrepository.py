# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stuffrepository.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(828, 554)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_0 = QtWidgets.QWidget()
        self.tab_0.setObjectName("tab_0")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget_stuffbatchnolist = QtWidgets.QTreeWidget(self.tab_0)
        self.treeWidget_stuffbatchnolist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_stuffbatchnolist.setObjectName("treeWidget_stuffbatchnolist")
        self.gridLayout_2.addWidget(self.treeWidget_stuffbatchnolist, 0, 0, 1, 1)
        self.treeWidget_stuffkindlist = QtWidgets.QTreeWidget(self.tab_0)
        self.treeWidget_stuffkindlist.setObjectName("treeWidget_stuffkindlist")
        self.gridLayout_2.addWidget(self.treeWidget_stuffkindlist, 1, 0, 1, 1)
        self.tabWidget.addTab(self.tab_0, "")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.tabWidget.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.tabWidget.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tabWidget, 4, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.radioButton_batchno = QtWidgets.QRadioButton(Form)
        self.radioButton_batchno.setChecked(True)
        self.radioButton_batchno.setObjectName("radioButton_batchno")
        self.horizontalLayout.addWidget(self.radioButton_batchno)
        self.radioButton_kind = QtWidgets.QRadioButton(Form)
        self.radioButton_kind.setObjectName("radioButton_kind")
        self.horizontalLayout.addWidget(self.radioButton_kind)
        self.gridLayout.addLayout(self.horizontalLayout, 2, 0, 1, 1)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(1, _translate("Form", "lrid"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(2, _translate("Form", "状态"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(3, _translate("Form", "物料"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(4, _translate("Form", "种类"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(5, _translate("Form", "类别"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(6, _translate("Form", "进厂批号"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(7, _translate("Form", "厂家批号"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(8, _translate("Form", "规格"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(9, _translate("Form", "包装规格"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(10, _translate("Form", "入库数量"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(11, _translate("Form", "剩余库存"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(12, _translate("Form", "单位"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(13, _translate("Form", "存放位置"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(14, _translate("Form", "生产日期"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(15, _translate("Form", "入库日期"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(16, _translate("Form", "过期日期"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(17, _translate("Form", "复检日期"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(18, _translate("Form", "供应商"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(19, _translate("Form", "生产厂家"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(20, _translate("Form", "含量"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(21, _translate("Form", "水分"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(22, _translate("Form", "相对密度"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(23, _translate("Form", "杂质"))
        self.treeWidget_stuffbatchnolist.headerItem().setText(24, _translate("Form", "仓管员"))
        self.treeWidget_stuffkindlist.headerItem().setText(0, _translate("Form", "种类"))
        self.treeWidget_stuffkindlist.headerItem().setText(1, _translate("Form", "入库数量"))
        self.treeWidget_stuffkindlist.headerItem().setText(2, _translate("Form", "剩余库存"))
        self.treeWidget_stuffkindlist.headerItem().setText(3, _translate("Form", "单位"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_0), _translate("Form", "全部"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_1), _translate("Form", "主材料"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Form", "前处理"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "辅材料"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "内包材"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Form", "外包材"))
        self.radioButton_batchno.setText(_translate("Form", "按物料批次排序"))
        self.radioButton_kind.setText(_translate("Form", "按物料类别排序"))
