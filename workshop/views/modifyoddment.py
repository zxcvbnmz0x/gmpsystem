# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'modifyoddment.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 163)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_accept = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_accept.sizePolicy().hasHeightForWidth())
        self.pushButton_accept.setSizePolicy(sizePolicy)
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.horizontalLayout.addWidget(self.pushButton_accept)
        self.pushButton_cancel = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_cancel.sizePolicy().hasHeightForWidth())
        self.pushButton_cancel.setSizePolicy(sizePolicy)
        self.pushButton_cancel.setObjectName("pushButton_cancel")
        self.horizontalLayout.addWidget(self.pushButton_cancel)
        self.gridLayout.addLayout(self.horizontalLayout, 3, 1, 1, 1)
        self.lineEdit_amount = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_amount.setObjectName("lineEdit_amount")
        self.gridLayout.addWidget(self.lineEdit_amount, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.comboBox_unit = QtWidgets.QComboBox(Dialog)
        self.comboBox_unit.setEditable(True)
        self.comboBox_unit.setObjectName("comboBox_unit")
        self.gridLayout.addWidget(self.comboBox_unit, 1, 1, 1, 1)
        self.dateEdit_regdate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_regdate.setCalendarPopup(True)
        self.dateEdit_regdate.setObjectName("dateEdit_regdate")
        self.gridLayout.addWidget(self.dateEdit_regdate, 2, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "编辑零头登记记录"))
        self.label_4.setText(_translate("Dialog", "登记日期："))
        self.pushButton_accept.setText(_translate("Dialog", "确认"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))
        self.label_2.setText(_translate("Dialog", "数量:"))
        self.label_3.setText(_translate("Dialog", "单位："))
