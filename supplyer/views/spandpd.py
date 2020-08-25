# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'spandpd.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(425, 130)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.supplyerid = QtWidgets.QLineEdit(Dialog)
        self.supplyerid.setObjectName("supplyerid")
        self.gridLayout.addWidget(self.supplyerid, 0, 3, 1, 1)
        self.producer = QtWidgets.QLineEdit(Dialog)
        self.producer.setObjectName("producer")
        self.gridLayout.addWidget(self.producer, 2, 3, 1, 1)
        self.supplyeridlabel = QtWidgets.QLabel(Dialog)
        self.supplyeridlabel.setObjectName("supplyeridlabel")
        self.gridLayout.addWidget(self.supplyeridlabel, 0, 0, 1, 1)
        self.supplyername = QtWidgets.QLineEdit(Dialog)
        self.supplyername.setObjectName("supplyername")
        self.gridLayout.addWidget(self.supplyername, 1, 3, 1, 1)
        self.producerlabel = QtWidgets.QLabel(Dialog)
        self.producerlabel.setObjectName("producerlabel")
        self.gridLayout.addWidget(self.producerlabel, 2, 0, 1, 1)
        self.supplyernamelabel = QtWidgets.QLabel(Dialog)
        self.supplyernamelabel.setObjectName("supplyernamelabel")
        self.gridLayout.addWidget(self.supplyernamelabel, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.acceptbutton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptbutton.sizePolicy().hasHeightForWidth())
        self.acceptbutton.setSizePolicy(sizePolicy)
        self.acceptbutton.setObjectName("acceptbutton")
        self.horizontalLayout_2.addWidget(self.acceptbutton)
        self.cancelbutton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelbutton.sizePolicy().hasHeightForWidth())
        self.cancelbutton.setSizePolicy(sizePolicy)
        self.cancelbutton.setObjectName("cancelbutton")
        self.horizontalLayout_2.addWidget(self.cancelbutton)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 3, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.supplyerid, self.supplyername)
        Dialog.setTabOrder(self.supplyername, self.producer)
        Dialog.setTabOrder(self.producer, self.acceptbutton)
        Dialog.setTabOrder(self.acceptbutton, self.cancelbutton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.supplyeridlabel.setText(_translate("Dialog", "供应商编号："))
        self.producerlabel.setText(_translate("Dialog", "生产厂家："))
        self.supplyernamelabel.setText(_translate("Dialog", "供应商名称："))
        self.acceptbutton.setText(_translate("Dialog", "确认"))
        self.cancelbutton.setText(_translate("Dialog", "取消"))
