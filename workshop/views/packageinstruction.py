# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'packageinstruction.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(821, 480)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 2, 1, 1)
        self.pushButton_bpexecutor = SignButton(Form)
        self.pushButton_bpexecutor.setEnabled(True)
        self.pushButton_bpexecutor.setText("")
        self.pushButton_bpexecutor.setObjectName("pushButton_bpexecutor")
        self.gridLayout.addWidget(self.pushButton_bpexecutor, 1, 5, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 1, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.pushButton_bpconstitutor = SignButton(Form)
        self.pushButton_bpconstitutor.setEnabled(False)
        self.pushButton_bpconstitutor.setText("")
        self.pushButton_bpconstitutor.setObjectName("pushButton_bpconstitutor")
        self.gridLayout.addWidget(self.pushButton_bpconstitutor, 1, 1, 1, 1)
        self.pushButton_bpwarrantor = SignButton(Form)
        self.pushButton_bpwarrantor.setEnabled(False)
        self.pushButton_bpwarrantor.setText("")
        self.pushButton_bpwarrantor.setObjectName("pushButton_bpwarrantor")
        self.gridLayout.addWidget(self.pushButton_bpwarrantor, 1, 3, 1, 1)
        self.dateEdit_bpconsdate = QtWidgets.QDateEdit(Form)
        self.dateEdit_bpconsdate.setEnabled(False)
        self.dateEdit_bpconsdate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dateEdit_bpconsdate.setStyleSheet("")
        self.dateEdit_bpconsdate.setReadOnly(True)
        self.dateEdit_bpconsdate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateEdit_bpconsdate.setObjectName("dateEdit_bpconsdate")
        self.gridLayout.addWidget(self.dateEdit_bpconsdate, 2, 1, 1, 1)
        self.dateEdit_bpwarrantdate = QtWidgets.QDateEdit(Form)
        self.dateEdit_bpwarrantdate.setEnabled(False)
        self.dateEdit_bpwarrantdate.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dateEdit_bpwarrantdate.setReadOnly(True)
        self.dateEdit_bpwarrantdate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.dateEdit_bpwarrantdate.setObjectName("dateEdit_bpwarrantdate")
        self.gridLayout.addWidget(self.dateEdit_bpwarrantdate, 2, 3, 1, 1)
        self.dateEdit_bpexecutedate = QtWidgets.QDateEdit(Form)
        self.dateEdit_bpexecutedate.setEnabled(True)
        self.dateEdit_bpexecutedate.setCalendarPopup(True)
        self.dateEdit_bpexecutedate.setObjectName("dateEdit_bpexecutedate")
        self.gridLayout.addWidget(self.dateEdit_bpexecutedate, 2, 5, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 6, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.label = QtWidgets.QLabel(Form)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.dateEdit_bpdate = QtWidgets.QDateEdit(Form)
        self.dateEdit_bpdate.setCalendarPopup(True)
        self.dateEdit_bpdate.setObjectName("dateEdit_bpdate")
        self.gridLayout.addWidget(self.dateEdit_bpdate, 2, 7, 1, 1)
        self.treeWidget_stufflist = QtWidgets.QTreeWidget(Form)
        self.treeWidget_stufflist.setIndentation(0)
        self.treeWidget_stufflist.setObjectName("treeWidget_stufflist")
        self.gridLayout.addWidget(self.treeWidget_stufflist, 0, 0, 1, 8)
        self.pushButton_accept = QtWidgets.QPushButton(Form)
        self.pushButton_accept.setObjectName("pushButton_accept")
        self.gridLayout.addWidget(self.pushButton_accept, 1, 7, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_4.setText(_translate("Form", "审核人："))
        self.label_5.setText(_translate("Form", "执行人："))
        self.label_2.setText(_translate("Form", "审核日期："))
        self.label_3.setText(_translate("Form", "执行日期："))
        self.label_6.setText(_translate("Form", "包装日期："))
        self.label_7.setText(_translate("Form", "制定日期："))
        self.label.setText(_translate("Form", "制定人："))
        self.treeWidget_stufflist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_stufflist.headerItem().setText(1, _translate("Form", "lrid"))
        self.treeWidget_stufflist.headerItem().setText(2, _translate("Form", "物料"))
        self.treeWidget_stufflist.headerItem().setText(3, _translate("Form", "进厂批号"))
        self.treeWidget_stufflist.headerItem().setText(4, _translate("Form", "含量规格"))
        self.treeWidget_stufflist.headerItem().setText(5, _translate("Form", "包装规格"))
        self.treeWidget_stufflist.headerItem().setText(6, _translate("Form", "计划量"))
        self.treeWidget_stufflist.headerItem().setText(7, _translate("Form", "含量/效价"))
        self.treeWidget_stufflist.headerItem().setText(8, _translate("Form", "水分"))
        self.treeWidget_stufflist.headerItem().setText(9, _translate("Form", "相对密度"))
        self.treeWidget_stufflist.headerItem().setText(10, _translate("Form", "杂质"))
        self.pushButton_accept.setText(_translate("Form", "保存"))
from lib.sign.signbutton import SignButton