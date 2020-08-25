# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stuffpicking.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(810, 587)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_refresh = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_refresh.sizePolicy().hasHeightForWidth())
        self.pushButton_refresh.setSizePolicy(sizePolicy)
        self.pushButton_refresh.setStyleSheet("")
        self.pushButton_refresh.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/logo/images/refresh.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_refresh.setIcon(icon)
        self.pushButton_refresh.setIconSize(QtCore.QSize(30, 30))
        self.pushButton_refresh.setObjectName("pushButton_refresh")
        self.horizontalLayout.addWidget(self.pushButton_refresh)
        self.printerButton = QtWidgets.QPushButton(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printerButton.sizePolicy().hasHeightForWidth())
        self.printerButton.setSizePolicy(sizePolicy)
        self.printerButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/logo/images/printer.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printerButton.setIcon(icon1)
        self.printerButton.setIconSize(QtCore.QSize(30, 30))
        self.printerButton.setObjectName("printerButton")
        self.horizontalLayout.addWidget(self.printerButton)
        self.gridLayout.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.countlabel = QtWidgets.QLabel(Form)
        self.countlabel.setObjectName("countlabel")
        self.gridLayout.addWidget(self.countlabel, 4, 0, 1, 1)
        self.stuffdrawpaperlist = QtWidgets.QTreeWidget(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(12)
        sizePolicy.setVerticalStretch(15)
        sizePolicy.setHeightForWidth(self.stuffdrawpaperlist.sizePolicy().hasHeightForWidth())
        self.stuffdrawpaperlist.setSizePolicy(sizePolicy)
        self.stuffdrawpaperlist.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.stuffdrawpaperlist.setObjectName("stuffdrawpaperlist")
        self.gridLayout.addWidget(self.stuffdrawpaperlist, 3, 0, 1, 15)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_apply = QtWidgets.QPushButton(Form)
        self.pushButton_apply.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.pushButton_apply.sizePolicy().hasHeightForWidth())
        self.pushButton_apply.setSizePolicy(sizePolicy)
        self.pushButton_apply.setObjectName("pushButton_apply")
        self.horizontalLayout_2.addWidget(self.pushButton_apply)
        self.pushButton_finish = QtWidgets.QPushButton(Form)
        self.pushButton_finish.setObjectName("pushButton_finish")
        self.horizontalLayout_2.addWidget(self.pushButton_finish)
        self.gridLayout.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton_refresh.setToolTip(_translate("Form", "<html><head/><body><p>刷新</p></body></html>"))
        self.printerButton.setToolTip(_translate("Form", "<html><head/><body><p>打印</p></body></html>"))
        self.countlabel.setText(_translate("Form", "共0条记录"))
        self.stuffdrawpaperlist.headerItem().setText(0, _translate("Form", "id"))
        self.stuffdrawpaperlist.headerItem().setText(1, _translate("Form", "ppid"))
        self.stuffdrawpaperlist.headerItem().setText(2, _translate("Form", "类别"))
        self.stuffdrawpaperlist.headerItem().setText(3, _translate("Form", "领料人"))
        self.stuffdrawpaperlist.headerItem().setText(4, _translate("Form", "申请时间"))
        self.stuffdrawpaperlist.headerItem().setText(5, _translate("Form", "发料人"))
        self.stuffdrawpaperlist.headerItem().setText(6, _translate("Form", "发料时间"))
        self.stuffdrawpaperlist.headerItem().setText(7, _translate("Form", "产品"))
        self.stuffdrawpaperlist.headerItem().setText(8, _translate("Form", "产品含量规格"))
        self.stuffdrawpaperlist.headerItem().setText(9, _translate("Form", "产品包装规格"))
        self.stuffdrawpaperlist.headerItem().setText(10, _translate("Form", "产品批号"))
        self.pushButton_apply.setText(_translate("Form", "已提交"))
        self.pushButton_finish.setText(_translate("Form", "已领取"))
import stuffimages_rc
