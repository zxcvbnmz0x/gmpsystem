# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cleanconfirmity_original.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(830, 290)
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setGeometry(QtCore.QRect(9, 9, 810, 261))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.lineEdit_postname = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_postname.setObjectName("lineEdit_postname")
        self.gridLayout_2.addWidget(self.lineEdit_postname, 0, 4, 1, 1)
        self.lineEdit_roomname = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_roomname.setObjectName("lineEdit_roomname")
        self.gridLayout_2.addWidget(self.lineEdit_roomname, 0, 1, 1, 1)
        self.pushButton_checker = SignButton(self.groupBox)
        self.pushButton_checker.setText("")
        self.pushButton_checker.setObjectName("pushButton_checker")
        self.gridLayout_2.addWidget(self.pushButton_checker, 4, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(22)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 2, 0, 1, 5)
        self.lineEdit_validdate = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_validdate.setObjectName("lineEdit_validdate")
        self.gridLayout_2.addWidget(self.lineEdit_validdate, 5, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 3, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 4, 0, 1, 1)
        self.lineEdit_product = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_product.setObjectName("lineEdit_product")
        self.gridLayout_2.addWidget(self.lineEdit_product, 1, 1, 1, 1)
        self.lineEdit_cleandate = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_cleandate.setObjectName("lineEdit_cleandate")
        self.gridLayout_2.addWidget(self.lineEdit_cleandate, 3, 4, 1, 1)
        self.lineEdit_checkdate = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_checkdate.setObjectName("lineEdit_checkdate")
        self.gridLayout_2.addWidget(self.lineEdit_checkdate, 4, 4, 1, 1)
        self.label_15 = QtWidgets.QLabel(self.groupBox)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName("label_15")
        self.gridLayout_2.addWidget(self.label_15, 3, 3, 1, 1)
        self.pushButton_cleaner = SignButton(self.groupBox)
        self.pushButton_cleaner.setText("")
        self.pushButton_cleaner.setObjectName("pushButton_cleaner")
        self.gridLayout_2.addWidget(self.pushButton_cleaner, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox)
        self.label_10.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 5, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 1, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 1, 3, 1, 1)
        self.label_14 = QtWidgets.QLabel(self.groupBox)
        self.label_14.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 4, 3, 1, 1)
        self.lineEdit_batchno = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit_batchno.setObjectName("lineEdit_batchno")
        self.gridLayout_2.addWidget(self.lineEdit_batchno, 1, 4, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout_2.addWidget(self.label_4, 0, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "清场合格证副本"))
        self.label_7.setText(_translate("Form", "清场合格证（正本）"))
        self.label_8.setText(_translate("Form", "清场者："))
        self.label_9.setText(_translate("Form", "检查者："))
        self.label_15.setText(_translate("Form", "清场日期："))
        self.label.setText(_translate("Form", "房间："))
        self.label_10.setText(_translate("Form", "有效期至："))
        self.label_3.setText(_translate("Form", "产品名："))
        self.label_6.setText(_translate("Form", "批号："))
        self.label_14.setText(_translate("Form", "检查日期："))
        self.label_4.setText(_translate("Form", "工序："))
from lib.sign.signbutton import SignButton
