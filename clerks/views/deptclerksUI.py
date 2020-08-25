# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'deptclerksUI.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_clerks(object):
    def setupUi(self, clerks):
        clerks.setObjectName("clerks")
        clerks.resize(781, 585)
        self.gridLayout = QtWidgets.QGridLayout(clerks)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.deptlist = QtWidgets.QTreeWidget(clerks)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(3)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.deptlist.sizePolicy().hasHeightForWidth())
        self.deptlist.setSizePolicy(sizePolicy)
        self.deptlist.setObjectName("deptlist")
        item_0 = QtWidgets.QTreeWidgetItem(self.deptlist)
        self.deptlist.header().setCascadingSectionResizes(True)
        self.deptlist.header().setDefaultSectionSize(80)
        self.gridLayout.addWidget(self.deptlist, 0, 0, 2, 1)
        self.incumbency = QtWidgets.QPushButton(clerks)
        self.incumbency.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.incumbency.sizePolicy().hasHeightForWidth())
        self.incumbency.setSizePolicy(sizePolicy)
        self.incumbency.setObjectName("incumbency")
        self.gridLayout.addWidget(self.incumbency, 0, 2, 1, 1)
        self.severance = QtWidgets.QPushButton(clerks)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.severance.sizePolicy().hasHeightForWidth())
        self.severance.setSizePolicy(sizePolicy)
        self.severance.setObjectName("severance")
        self.gridLayout.addWidget(self.severance, 0, 3, 1, 1)
        self.userlist = QtWidgets.QTreeWidget(clerks)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(8)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.userlist.sizePolicy().hasHeightForWidth())
        self.userlist.setSizePolicy(sizePolicy)
        self.userlist.setIndentation(0)
        self.userlist.setObjectName("userlist")
        self.userlist.header().setCascadingSectionResizes(True)
        self.userlist.header().setDefaultSectionSize(30)
        self.gridLayout.addWidget(self.userlist, 1, 2, 1, 3)

        self.retranslateUi(clerks)
        QtCore.QMetaObject.connectSlotsByName(clerks)

    def retranslateUi(self, clerks):
        _translate = QtCore.QCoreApplication.translate
        clerks.setWindowTitle(_translate("clerks", "Form"))
        self.deptlist.headerItem().setText(0, _translate("clerks", "部门编号"))
        self.deptlist.headerItem().setText(1, _translate("clerks", "部门名称"))
        __sortingEnabled = self.deptlist.isSortingEnabled()
        self.deptlist.setSortingEnabled(False)
        self.deptlist.topLevelItem(0).setText(0, _translate("clerks", "全部部门"))
        self.deptlist.setSortingEnabled(__sortingEnabled)
        self.incumbency.setText(_translate("clerks", "在职"))
        self.severance.setText(_translate("clerks", "离职"))
        self.userlist.headerItem().setText(0, _translate("clerks", "编号"))
        self.userlist.headerItem().setText(1, _translate("clerks", "姓名"))
        self.userlist.headerItem().setText(2, _translate("clerks", "性别"))
        self.userlist.headerItem().setText(3, _translate("clerks", "出生日期"))
        self.userlist.headerItem().setText(4, _translate("clerks", "雇佣日期"))
        self.userlist.headerItem().setText(5, _translate("clerks", "文化程度"))
        self.userlist.headerItem().setText(6, _translate("clerks", "婚姻状况"))
        self.userlist.headerItem().setText(7, _translate("clerks", "身份证号码"))
        self.userlist.headerItem().setText(8, _translate("clerks", "联系方式"))
