# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'production_order.ui'
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
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 4, 1, 1)
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 2, 1, 1)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 6, 1, 1)
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 2, 4, 1, 1)
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.label_draft_date = QtWidgets.QLabel(Form)
        self.label_draft_date.setText("")
        self.label_draft_date.setObjectName("label_draft_date")
        self.gridLayout.addWidget(self.label_draft_date, 2, 1, 1, 1)
        self.label_review_date = QtWidgets.QLabel(Form)
        self.label_review_date.setText("")
        self.label_review_date.setObjectName("label_review_date")
        self.gridLayout.addWidget(self.label_review_date, 2, 3, 1, 1)
        self.label_check_date = QtWidgets.QLabel(Form)
        self.label_check_date.setText("")
        self.label_check_date.setObjectName("label_check_date")
        self.gridLayout.addWidget(self.label_check_date, 2, 5, 1, 1)
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 2, 6, 1, 1)
        self.label_exectu_date = QtWidgets.QLabel(Form)
        self.label_exectu_date.setText("")
        self.label_exectu_date.setObjectName("label_exectu_date")
        self.gridLayout.addWidget(self.label_exectu_date, 2, 7, 1, 1)
        self.treeWidget_stufflist = QtWidgets.QTreeWidget(Form)
        self.treeWidget_stufflist.setObjectName("treeWidget_stufflist")
        self.gridLayout.addWidget(self.treeWidget_stufflist, 0, 0, 1, 8)
        self.pushButton_stufflist = SignButton(Form)
        self.pushButton_stufflist.setText("")
        self.pushButton_stufflist.setObjectName("pushButton_stufflist")
        self.gridLayout.addWidget(self.pushButton_stufflist, 1, 1, 1, 1)
        self.pushButton_reviewer = SignButton(Form)
        self.pushButton_reviewer.setText("")
        self.pushButton_reviewer.setObjectName("pushButton_reviewer")
        self.gridLayout.addWidget(self.pushButton_reviewer, 1, 3, 1, 1)
        self.pushButton_QAchecker = SignButton(Form)
        self.pushButton_QAchecker.setText("")
        self.pushButton_QAchecker.setObjectName("pushButton_QAchecker")
        self.gridLayout.addWidget(self.pushButton_QAchecker, 1, 5, 1, 1)
        self.pushButton_executor = SignButton(Form)
        self.pushButton_executor.setText("")
        self.pushButton_executor.setObjectName("pushButton_executor")
        self.gridLayout.addWidget(self.pushButton_executor, 1, 7, 1, 1)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "制订人："))
        self.label_3.setText(_translate("Form", "QA复核："))
        self.label_2.setText(_translate("Form", "审核人："))
        self.label_4.setText(_translate("Form", "执行人："))
        self.label_5.setText(_translate("Form", "下达日期："))
        self.label_7.setText(_translate("Form", "复核日期："))
        self.label_6.setText(_translate("Form", "审核日期："))
        self.label_8.setText(_translate("Form", "执行日期；"))
        self.treeWidget_stufflist.headerItem().setText(0, _translate("Form", "id"))
        self.treeWidget_stufflist.headerItem().setText(1, _translate("Form", "编号"))
        self.treeWidget_stufflist.headerItem().setText(2, _translate("Form", "名称"))
        self.treeWidget_stufflist.headerItem().setText(3, _translate("Form", "类别"))
        self.treeWidget_stufflist.headerItem().setText(4, _translate("Form", "来源"))
        self.treeWidget_stufflist.headerItem().setText(5, _translate("Form", "包装规格"))
        self.treeWidget_stufflist.headerItem().setText(6, _translate("Form", "进厂批号"))
        self.treeWidget_stufflist.headerItem().setText(7, _translate("Form", "计划量"))
        self.treeWidget_stufflist.headerItem().setText(8, _translate("Form", "单位"))
        self.treeWidget_stufflist.headerItem().setText(9, _translate("Form", "含量"))
        self.treeWidget_stufflist.headerItem().setText(10, _translate("Form", "水分"))
        self.treeWidget_stufflist.headerItem().setText(11, _translate("Form", "杂质"))
        self.treeWidget_stufflist.headerItem().setText(12, _translate("Form", "相对密度"))
from lib.sign.signbutton import SignButton