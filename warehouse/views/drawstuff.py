# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'drawstuff.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.groupBox_3 = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget_drawstuff = MyTreeWidget(self.groupBox_3)
        self.treeWidget_drawstuff.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeWidget_drawstuff.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_drawstuff.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.treeWidget_drawstuff.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_drawstuff.setIndentation(0)
        self.treeWidget_drawstuff.setObjectName("treeWidget_drawstuff")
        self.gridLayout_2.addWidget(self.treeWidget_drawstuff, 0, 0, 1, 3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, 0, 3, 4)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_accept = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_accept.sizePolicy().hasHeightForWidth())
        self.pushButton_accept.setSizePolicy(sizePolicy)
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.horizontalLayout.addWidget(self.pushButton_accept)
        self.pushButton_cancel = QtWidgets.QPushButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.gridLayout_2.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_3, 1, 0, 1, 3)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.treeWidget_formula = MyTreeWidget(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.treeWidget_formula.sizePolicy().hasHeightForWidth())
        self.treeWidget_formula.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.treeWidget_formula.setFont(font)
        self.treeWidget_formula.setStyleSheet("")
        self.treeWidget_formula.setTextElideMode(QtCore.Qt.ElideRight)
        self.treeWidget_formula.setIndentation(0)
        self.treeWidget_formula.setWordWrap(True)
        self.treeWidget_formula.setObjectName("treeWidget_formula")
        self.treeWidget_formula.header().setCascadingSectionResizes(False)
        self.treeWidget_formula.header().setHighlightSections(False)
        self.treeWidget_formula.header().setSortIndicatorShown(False)
        self.gridLayout_3.addWidget(self.treeWidget_formula, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.treeWidget_stuffrepository = MyTreeWidget(self.groupBox_2)
        self.treeWidget_stuffrepository.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.treeWidget_stuffrepository.setIndentation(0)
        self.treeWidget_stuffrepository.setObjectName("treeWidget_stuffrepository")
        self.gridLayout_4.addWidget(self.treeWidget_stuffrepository, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 0, 2, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "领取物料"))
        self.groupBox_3.setTitle(_translate("Dialog", "待领取物料"))
        self.treeWidget_drawstuff.headerItem().setText(0, _translate("Dialog", "id"))
        self.treeWidget_drawstuff.headerItem().setText(1, _translate("Dialog", "物料种类"))
        self.treeWidget_drawstuff.headerItem().setText(2, _translate("Dialog", "物料名称"))
        self.treeWidget_drawstuff.headerItem().setText(3, _translate("Dialog", "含量规格"))
        self.treeWidget_drawstuff.headerItem().setText(4, _translate("Dialog", "包装规格"))
        self.treeWidget_drawstuff.headerItem().setText(5, _translate("Dialog", "计划量"))
        self.treeWidget_drawstuff.headerItem().setText(6, _translate("Dialog", "单位"))
        self.treeWidget_drawstuff.headerItem().setText(7, _translate("Dialog", "实际量"))
        self.treeWidget_drawstuff.headerItem().setText(8, _translate("Dialog", "单位"))
        self.treeWidget_drawstuff.headerItem().setText(9, _translate("Dialog", "领取量"))
        self.treeWidget_drawstuff.headerItem().setText(10, _translate("Dialog", "单位"))
        self.treeWidget_drawstuff.headerItem().setText(11, _translate("Dialog", "进厂批号"))
        self.treeWidget_drawstuff.headerItem().setText(12, _translate("Dialog", "厂家批号"))
        self.treeWidget_drawstuff.headerItem().setText(13, _translate("Dialog", "含量/效价"))
        self.treeWidget_drawstuff.headerItem().setText(14, _translate("Dialog", "水分"))
        self.treeWidget_drawstuff.headerItem().setText(15, _translate("Dialog", "相对密度"))
        self.treeWidget_drawstuff.headerItem().setText(16, _translate("Dialog", "杂质"))
        self.treeWidget_drawstuff.headerItem().setText(17, _translate("Dialog", "损耗限度"))
        self.treeWidget_drawstuff.headerItem().setText(18, _translate("Dialog", "供应商"))
        self.treeWidget_drawstuff.headerItem().setText(19, _translate("Dialog", "生产厂家"))
        self.treeWidget_drawstuff.headerItem().setText(20, _translate("Dialog", "新的计划量"))
        self.treeWidget_drawstuff.headerItem().setText(21, _translate("Dialog", "原始的实际量"))
        self.treeWidget_drawstuff.headerItem().setText(22, _translate("Dialog", "精度"))
        self.pushButton_accept.setText(_translate("Dialog", "确认领料"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消领料"))
        self.groupBox.setTitle(_translate("Dialog", "产品配方"))
        self.treeWidget_formula.headerItem().setText(0, _translate("Dialog", "id"))
        self.treeWidget_formula.headerItem().setText(1, _translate("Dialog", "类别"))
        self.treeWidget_formula.headerItem().setText(2, _translate("Dialog", "物料种类"))
        self.treeWidget_formula.headerItem().setText(3, _translate("Dialog", "配方"))
        self.treeWidget_formula.headerItem().setText(4, _translate("Dialog", "计划量公式"))
        self.treeWidget_formula.headerItem().setText(5, _translate("Dialog", "实际量公式"))
        self.treeWidget_formula.headerItem().setText(6, _translate("Dialog", "领取量公式"))
        self.treeWidget_formula.headerItem().setText(7, _translate("Dialog", "领料精度"))
        self.treeWidget_formula.headerItem().setText(8, _translate("Dialog", "损耗限度"))
        self.treeWidget_formula.headerItem().setText(9, _translate("Dialog", "发料完成"))
        self.groupBox_2.setTitle(_translate("Dialog", "库存列表"))
        self.treeWidget_stuffrepository.headerItem().setText(0, _translate("Dialog", "id"))
        self.treeWidget_stuffrepository.headerItem().setText(1, _translate("Dialog", "物料种类"))
        self.treeWidget_stuffrepository.headerItem().setText(2, _translate("Dialog", "物料名称"))
        self.treeWidget_stuffrepository.headerItem().setText(3, _translate("Dialog", "含量规格"))
        self.treeWidget_stuffrepository.headerItem().setText(4, _translate("Dialog", "包装规格"))
        self.treeWidget_stuffrepository.headerItem().setText(5, _translate("Dialog", "进厂批号"))
        self.treeWidget_stuffrepository.headerItem().setText(6, _translate("Dialog", "厂家批号"))
        self.treeWidget_stuffrepository.headerItem().setText(7, _translate("Dialog", "库存剩余量"))
        self.treeWidget_stuffrepository.headerItem().setText(8, _translate("Dialog", "库存可使用量"))
        self.treeWidget_stuffrepository.headerItem().setText(9, _translate("Dialog", "供应商"))
        self.treeWidget_stuffrepository.headerItem().setText(10, _translate("Dialog", "生产厂家"))
        self.treeWidget_stuffrepository.headerItem().setText(11, _translate("Dialog", "含量/效价"))
        self.treeWidget_stuffrepository.headerItem().setText(12, _translate("Dialog", "水分"))
        self.treeWidget_stuffrepository.headerItem().setText(13, _translate("Dialog", "相对密度"))
        self.treeWidget_stuffrepository.headerItem().setText(14, _translate("Dialog", "杂质"))
        self.treeWidget_stuffrepository.headerItem().setText(15, _translate("Dialog", "领料实际量"))
from lib.mywidget.mytreewidget import MyTreeWidget