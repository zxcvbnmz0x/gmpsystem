# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'sampling.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(500, 520)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
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
        self.gridLayout.addLayout(self.horizontalLayout, 8, 1, 1, 1)
        self.label_chkitem = QtWidgets.QLabel(Dialog)
        self.label_chkitem.setText("")
        self.label_chkitem.setObjectName("label_chkitem")
        self.gridLayout.addWidget(self.label_chkitem, 0, 1, 1, 2)
        self.label_checkamount = QtWidgets.QLabel(Dialog)
        self.label_checkamount.setText("")
        self.label_checkamount.setObjectName("label_checkamount")
        self.gridLayout.addWidget(self.label_checkamount, 1, 1, 1, 2)
        self.label_samplesource = QtWidgets.QLabel(Dialog)
        self.label_samplesource.setText("")
        self.label_samplesource.setObjectName("label_samplesource")
        self.gridLayout.addWidget(self.label_samplesource, 3, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 0, 1, 1)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 4, 0, 1, 1)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 3, 0, 1, 1)
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 6, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 5, 0, 1, 1)
        self.label_applyer = QtWidgets.QLabel(Dialog)
        self.label_applyer.setText("")
        self.label_applyer.setObjectName("label_applyer")
        self.gridLayout.addWidget(self.label_applyer, 2, 1, 1, 1)
        self.lineEdit_remark = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_remark.setObjectName("lineEdit_remark")
        self.gridLayout.addWidget(self.lineEdit_remark, 7, 1, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_sampleamount = QtWidgets.QLineEdit(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_sampleamount.sizePolicy().hasHeightForWidth())
        self.lineEdit_sampleamount.setSizePolicy(sizePolicy)
        self.lineEdit_sampleamount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_sampleamount.setObjectName("lineEdit_sampleamount")
        self.horizontalLayout_2.addWidget(self.lineEdit_sampleamount)
        self.label_sampleunit = QtWidgets.QLabel(Dialog)
        self.label_sampleunit.setText("")
        self.label_sampleunit.setObjectName("label_sampleunit")
        self.horizontalLayout_2.addWidget(self.label_sampleunit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 6, 1, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.treeWidget_labitem = QtWidgets.QTreeWidget(self.groupBox)
        self.treeWidget_labitem.setIndentation(0)
        self.treeWidget_labitem.setObjectName("treeWidget_labitem")
        self.gridLayout_2.addWidget(self.treeWidget_labitem, 0, 0, 1, 1)
        self.gridLayout.addWidget(self.groupBox, 9, 0, 1, 2)
        self.dateEdit_applydate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_applydate.setEnabled(False)
        self.dateEdit_applydate.setObjectName("dateEdit_applydate")
        self.gridLayout.addWidget(self.dateEdit_applydate, 4, 1, 1, 1)
        self.dateEdit_sampledate = QtWidgets.QDateEdit(Dialog)
        self.dateEdit_sampledate.setCalendarPopup(True)
        self.dateEdit_sampledate.setObjectName("dateEdit_sampledate")
        self.gridLayout.addWidget(self.dateEdit_sampledate, 5, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "取样记录"))
        self.pushButton_accept.setText(_translate("Dialog", "取样签名"))
        self.pushButton_cancel.setText(_translate("Dialog", "取消"))
        self.label_8.setText(_translate("Dialog", "取样备注："))
        self.label_7.setText(_translate("Dialog", "请验人："))
        self.label_6.setText(_translate("Dialog", "检品数量："))
        self.label_3.setText(_translate("Dialog", "请验时间："))
        self.label.setText(_translate("Dialog", "待检物："))
        self.label_2.setText(_translate("Dialog", "样品来源："))
        self.label_5.setText(_translate("Dialog", "样品数量："))
        self.label_4.setText(_translate("Dialog", "取样时间："))
        self.groupBox.setTitle(_translate("Dialog", "待检项目"))
        self.treeWidget_labitem.headerItem().setText(0, _translate("Dialog", "id"))
        self.treeWidget_labitem.headerItem().setText(1, _translate("Dialog", "类别"))
        self.treeWidget_labitem.headerItem().setText(2, _translate("Dialog", "项目"))
