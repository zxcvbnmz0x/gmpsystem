# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'selectproductline.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 320)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.cancelButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout.addWidget(self.cancelButton, 2, 2, 1, 1)
        self.productlinelist = QtWidgets.QTreeWidget(Dialog)
        self.productlinelist.setObjectName("productlinelist")
        self.productlinelist.header().setCascadingSectionResizes(True)
        self.gridLayout.addWidget(self.productlinelist, 1, 0, 1, 4)
        self.acceptButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptButton.sizePolicy().hasHeightForWidth())
        self.acceptButton.setSizePolicy(sizePolicy)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout.addWidget(self.acceptButton, 2, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 2, 3, 1, 1)
        self.countlabel = QtWidgets.QLabel(Dialog)
        self.countlabel.setObjectName("countlabel")
        self.gridLayout.addWidget(self.countlabel, 3, 0, 1, 4)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.productlinelist, self.acceptButton)
        Dialog.setTabOrder(self.acceptButton, self.cancelButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "选择生产线"))
        self.cancelButton.setText(_translate("Dialog", "取消"))
        self.productlinelist.headerItem().setText(0, _translate("Dialog", "id"))
        self.productlinelist.headerItem().setText(1, _translate("Dialog", "生产线名称"))
        self.productlinelist.headerItem().setText(2, _translate("Dialog", "车间编号"))
        self.productlinelist.headerItem().setText(3, _translate("Dialog", "车间名称"))
        self.acceptButton.setText(_translate("Dialog", "确认"))
        self.countlabel.setText(_translate("Dialog", "共0条记录"))
