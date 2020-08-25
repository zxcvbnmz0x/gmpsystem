# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'material_requisition.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(0, 0))
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 2, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 3, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 3, 2, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 2, 1, 1)
        self.label_submit_time = QtWidgets.QLabel(Form)
        self.label_submit_time.setText("")
        self.label_submit_time.setObjectName("label_submit_time")
        self.gridLayout.addWidget(self.label_submit_time, 3, 1, 1, 1)
        self.pushButton_submit = QtWidgets.QPushButton(Form)
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.gridLayout.addWidget(self.pushButton_submit, 3, 4, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 5, 1, 1)
        self.label_status = QtWidgets.QLabel(Form)
        self.label_status.setText("")
        self.label_status.setObjectName("label_status")
        self.gridLayout.addWidget(self.label_status, 2, 6, 1, 1)
        self.treeWidget_stufflist = QtWidgets.QTreeWidget(Form)
        self.treeWidget_stufflist.setObjectName("treeWidget_stufflist")
        self.treeWidget_stufflist.headerItem().setText(0, "1")
        self.gridLayout.addWidget(self.treeWidget_stufflist, 0, 0, 1, 9)
        self.label_operate_time = QtWidgets.QLabel(Form)
        self.label_operate_time.setText("")
        self.label_operate_time.setObjectName("label_operate_time")
        self.gridLayout.addWidget(self.label_operate_time, 3, 3, 1, 1)
        self.pushButton_submiter = SignButton(Form)
        self.pushButton_submiter.setText("")
        self.pushButton_submiter.setObjectName("pushButton_submiter")
        self.gridLayout.addWidget(self.pushButton_submiter, 2, 1, 1, 1)
        self.pushButton_operator = SignButton(Form)
        self.pushButton_operator.setText("")
        self.pushButton_operator.setObjectName("pushButton_operator")
        self.gridLayout.addWidget(self.pushButton_operator, 2, 3, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "领料人："))
        self.label_5.setText(_translate("Form", "领料时间；"))
        self.label_7.setText(_translate("Form", "发料时间："))
        self.label_2.setText(_translate("Form", "发料人："))
        self.pushButton_submit.setText(_translate("Form", "提交"))
        self.label_3.setText(_translate("Form", "状态："))
from lib.sign.signbutton import SignButton
