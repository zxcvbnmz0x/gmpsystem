# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'productdetail.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 480)
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.tab = QtWidgets.QTabWidget(Dialog)
        self.tab.setEnabled(True)
        self.tab.setTabsClosable(False)
        self.tab.setMovable(False)
        self.tab.setTabBarAutoHide(False)
        self.tab.setObjectName("tab")
        self.tab_1 = QtWidgets.QWidget()
        self.tab_1.setObjectName("tab_1")
        self.gridLayout_6 = QtWidgets.QGridLayout(self.tab_1)
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_1)
        self.groupBox_4.setObjectName("groupBox_4")
        self.gridLayout_11 = QtWidgets.QGridLayout(self.groupBox_4)
        self.gridLayout_11.setObjectName("gridLayout_11")
        self.workshoplabel = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workshoplabel.sizePolicy().hasHeightForWidth())
        self.workshoplabel.setSizePolicy(sizePolicy)
        self.workshoplabel.setObjectName("workshoplabel")
        self.gridLayout_11.addWidget(self.workshoplabel, 0, 0, 1, 1)
        self.workshop = QtWidgets.QToolButton(self.groupBox_4)
        self.workshop.setObjectName("workshop")
        self.gridLayout_11.addWidget(self.workshop, 0, 1, 1, 1)
        self.productionlinelabel = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.productionlinelabel.sizePolicy().hasHeightForWidth())
        self.productionlinelabel.setSizePolicy(sizePolicy)
        self.productionlinelabel.setObjectName("productionlinelabel")
        self.gridLayout_11.addWidget(self.productionlinelabel, 1, 0, 1, 1)
        self.productionline = QtWidgets.QLabel(self.groupBox_4)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.productionline.sizePolicy().hasHeightForWidth())
        self.productionline.setSizePolicy(sizePolicy)
        self.productionline.setText("")
        self.productionline.setObjectName("productionline")
        self.gridLayout_11.addWidget(self.productionline, 1, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_4, 9, 1, 1, 2)
        self.qrtype = QtWidgets.QGroupBox(self.tab_1)
        self.qrtype.setObjectName("qrtype")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.qrtype)
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButton = QtWidgets.QRadioButton(self.qrtype)
        self.radioButton.setObjectName("radioButton")
        self.verticalLayout.addWidget(self.radioButton)
        self.radioButton_2 = QtWidgets.QRadioButton(self.qrtype)
        self.radioButton_2.setObjectName("radioButton_2")
        self.verticalLayout.addWidget(self.radioButton_2)
        self.radioButton_3 = QtWidgets.QRadioButton(self.qrtype)
        self.radioButton_3.setObjectName("radioButton_3")
        self.verticalLayout.addWidget(self.radioButton_3)
        self.gridLayout_6.addWidget(self.qrtype, 4, 3, 4, 2)
        self.packagelabel = QtWidgets.QLabel(self.tab_1)
        self.packagelabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.packagelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.packagelabel.setObjectName("packagelabel")
        self.gridLayout_6.addWidget(self.packagelabel, 8, 1, 1, 1)
        self.package_2 = QtWidgets.QLineEdit(self.tab_1)
        self.package_2.setObjectName("package_2")
        self.gridLayout_6.addWidget(self.package_2, 8, 2, 1, 1)
        self.acceptButton = QtWidgets.QPushButton(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptButton.sizePolicy().hasHeightForWidth())
        self.acceptButton.setSizePolicy(sizePolicy)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout_6.addWidget(self.acceptButton, 10, 3, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_6.addWidget(self.cancelButton, 10, 4, 1, 1)
        self.medkindlabel = QtWidgets.QLabel(self.tab_1)
        self.medkindlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.medkindlabel.setObjectName("medkindlabel")
        self.gridLayout_6.addWidget(self.medkindlabel, 0, 3, 1, 1)
        self.checkunitlabel = QtWidgets.QLabel(self.tab_1)
        self.checkunitlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.checkunitlabel.setObjectName("checkunitlabel")
        self.gridLayout_6.addWidget(self.checkunitlabel, 1, 3, 1, 1)
        self.idlabel = QtWidgets.QLabel(self.tab_1)
        self.idlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.idlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.idlabel.setObjectName("idlabel")
        self.gridLayout_6.addWidget(self.idlabel, 0, 1, 1, 1)
        self.namelabel = QtWidgets.QLabel(self.tab_1)
        self.namelabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.namelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.namelabel.setObjectName("namelabel")
        self.gridLayout_6.addWidget(self.namelabel, 1, 1, 1, 1)
        self.spec = QtWidgets.QLineEdit(self.tab_1)
        self.spec.setObjectName("spec")
        self.gridLayout_6.addWidget(self.spec, 6, 2, 1, 1)
        self.inputlabel = QtWidgets.QLabel(self.tab_1)
        self.inputlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.inputlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.inputlabel.setObjectName("inputlabel")
        self.gridLayout_6.addWidget(self.inputlabel, 5, 1, 1, 1)
        self.inputcode = QtWidgets.QLineEdit(self.tab_1)
        self.inputcode.setObjectName("inputcode")
        self.gridLayout_6.addWidget(self.inputcode, 5, 2, 1, 1)
        self.allownolabel = QtWidgets.QLabel(self.tab_1)
        self.allownolabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allownolabel.setObjectName("allownolabel")
        self.gridLayout_6.addWidget(self.allownolabel, 4, 1, 1, 1)
        self.allowno = QtWidgets.QLineEdit(self.tab_1)
        self.allowno.setObjectName("allowno")
        self.gridLayout_6.addWidget(self.allowno, 4, 2, 1, 1)
        self.prodid = QtWidgets.QLineEdit(self.tab_1)
        self.prodid.setObjectName("prodid")
        self.gridLayout_6.addWidget(self.prodid, 0, 2, 1, 1)
        self.externalnolabel = QtWidgets.QLabel(self.tab_1)
        self.externalnolabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.externalnolabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.externalnolabel.setObjectName("externalnolabel")
        self.gridLayout_6.addWidget(self.externalnolabel, 2, 1, 1, 1)
        self.externalno = QtWidgets.QLineEdit(self.tab_1)
        self.externalno.setObjectName("externalno")
        self.gridLayout_6.addWidget(self.externalno, 2, 2, 1, 1)
        self.kindlabel = QtWidgets.QLabel(self.tab_1)
        self.kindlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.kindlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.kindlabel.setObjectName("kindlabel")
        self.gridLayout_6.addWidget(self.kindlabel, 3, 1, 1, 1)
        self.speclabel = QtWidgets.QLabel(self.tab_1)
        self.speclabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.speclabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.speclabel.setObjectName("speclabel")
        self.gridLayout_6.addWidget(self.speclabel, 6, 1, 1, 1)
        self.prodname = QtWidgets.QLineEdit(self.tab_1)
        self.prodname.setObjectName("prodname")
        self.gridLayout_6.addWidget(self.prodname, 1, 2, 1, 1)
        self.commonname = QtWidgets.QLineEdit(self.tab_1)
        self.commonname.setObjectName("commonname")
        self.gridLayout_6.addWidget(self.commonname, 3, 2, 1, 1)
        self.packageLvlabel = QtWidgets.QLabel(self.tab_1)
        self.packageLvlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.packageLvlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.packageLvlabel.setObjectName("packageLvlabel")
        self.gridLayout_6.addWidget(self.packageLvlabel, 7, 1, 1, 1)
        self.checkunit = QtWidgets.QComboBox(self.tab_1)
        self.checkunit.setEditable(False)
        self.checkunit.setObjectName("checkunit")
        self.checkunit.addItem("")
        self.checkunit.addItem("")
        self.checkunit.addItem("")
        self.checkunit.addItem("")
        self.gridLayout_6.addWidget(self.checkunit, 1, 4, 1, 1)
        self.packageLv = QtWidgets.QComboBox(self.tab_1)
        self.packageLv.setObjectName("packageLv")
        self.packageLv.addItem("")
        self.packageLv.addItem("")
        self.packageLv.addItem("")
        self.packageLv.addItem("")
        self.gridLayout_6.addWidget(self.packageLv, 7, 2, 1, 1)
        self.expiredlabel = QtWidgets.QLabel(self.tab_1)
        self.expiredlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.expiredlabel.setObjectName("expiredlabel")
        self.gridLayout_6.addWidget(self.expiredlabel, 2, 3, 1, 1)
        self.expireddates = QtWidgets.QLineEdit(self.tab_1)
        self.expireddates.setObjectName("expireddates")
        self.gridLayout_6.addWidget(self.expireddates, 2, 4, 1, 1)
        self.storagelabel = QtWidgets.QLabel(self.tab_1)
        self.storagelabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.storagelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.storagelabel.setObjectName("storagelabel")
        self.gridLayout_6.addWidget(self.storagelabel, 3, 3, 1, 1)
        self.storage = QtWidgets.QLineEdit(self.tab_1)
        self.storage.setObjectName("storage")
        self.gridLayout_6.addWidget(self.storage, 3, 4, 1, 1)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName("groupBox_3")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.groupBox_3)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.bworkshoplabel = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bworkshoplabel.sizePolicy().hasHeightForWidth())
        self.bworkshoplabel.setSizePolicy(sizePolicy)
        self.bworkshoplabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.bworkshoplabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bworkshoplabel.setObjectName("bworkshoplabel")
        self.gridLayout_10.addWidget(self.bworkshoplabel, 0, 0, 1, 1)
        self.bproductionlinelabel = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bproductionlinelabel.sizePolicy().hasHeightForWidth())
        self.bproductionlinelabel.setSizePolicy(sizePolicy)
        self.bproductionlinelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.bproductionlinelabel.setObjectName("bproductionlinelabel")
        self.gridLayout_10.addWidget(self.bproductionlinelabel, 1, 0, 1, 1)
        self.bworkshop = QtWidgets.QToolButton(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bworkshop.sizePolicy().hasHeightForWidth())
        self.bworkshop.setSizePolicy(sizePolicy)
        self.bworkshop.setObjectName("bworkshop")
        self.gridLayout_10.addWidget(self.bworkshop, 0, 1, 1, 1)
        self.bproductionline = QtWidgets.QLabel(self.groupBox_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bproductionline.sizePolicy().hasHeightForWidth())
        self.bproductionline.setSizePolicy(sizePolicy)
        self.bproductionline.setText("")
        self.bproductionline.setObjectName("bproductionline")
        self.gridLayout_10.addWidget(self.bproductionline, 1, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_3, 9, 3, 1, 2)
        self.medkind = QtWidgets.QComboBox(self.tab_1)
        self.medkind.setEditable(True)
        self.medkind.setObjectName("medkind")
        self.gridLayout_6.addWidget(self.medkind, 0, 4, 1, 1)
        self.tab.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.formula = QtWidgets.QTreeWidget(self.tab_2)
        self.formula.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.formula.setObjectName("formula")
        self.gridLayout_5.addWidget(self.formula, 0, 0, 1, 1)
        self.tab.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.precheckitem = QtWidgets.QTreeWidget(self.tab_3)
        self.precheckitem.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.precheckitem.setObjectName("precheckitem")
        self.gridLayout_4.addWidget(self.precheckitem, 0, 0, 1, 1)
        self.tab.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.prodcheckitem = QtWidgets.QTreeWidget(self.tab_4)
        self.prodcheckitem.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.prodcheckitem.setObjectName("prodcheckitem")
        self.gridLayout_3.addWidget(self.prodcheckitem, 0, 0, 1, 1)
        self.tab.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_7 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_7.setObjectName("gridLayout_7")
        self.samplecheckitem = QtWidgets.QTreeWidget(self.tab_5)
        self.samplecheckitem.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.samplecheckitem.setObjectName("samplecheckitem")
        self.gridLayout_7.addWidget(self.samplecheckitem, 0, 0, 1, 1)
        self.tab.addTab(self.tab_5, "")
        self.tab_6 = QtWidgets.QWidget()
        self.tab_6.setObjectName("tab_6")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_6)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName("groupBox_2")
        self.gridLayout_9 = QtWidgets.QGridLayout(self.groupBox_2)
        self.gridLayout_9.setObjectName("gridLayout_9")
        self.productimage = QtWidgets.QLabel(self.groupBox_2)
        self.productimage.setText("")
        self.productimage.setObjectName("productimage")
        self.gridLayout_9.addWidget(self.productimage, 0, 0, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.groupBox = QtWidgets.QGroupBox(self.tab_6)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_8 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_8.setObjectName("gridLayout_8")
        self.labellist = QtWidgets.QTreeWidget(self.groupBox)
        self.labellist.setObjectName("labellist")
        self.gridLayout_8.addWidget(self.labellist, 1, 0, 1, 3)
        self.labelvaildButton = QtWidgets.QPushButton(self.groupBox)
        self.labelvaildButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelvaildButton.sizePolicy().hasHeightForWidth())
        self.labelvaildButton.setSizePolicy(sizePolicy)
        self.labelvaildButton.setObjectName("labelvaildButton")
        self.gridLayout_8.addWidget(self.labelvaildButton, 0, 0, 1, 1)
        self.labelinvaildButton = QtWidgets.QPushButton(self.groupBox)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelinvaildButton.sizePolicy().hasHeightForWidth())
        self.labelinvaildButton.setSizePolicy(sizePolicy)
        self.labelinvaildButton.setObjectName("labelinvaildButton")
        self.gridLayout_8.addWidget(self.labelinvaildButton, 0, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox, 0, 0, 1, 1)
        self.tab.addTab(self.tab_6, "")
        self.gridLayout.addWidget(self.tab, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.prodid, self.prodname)
        Dialog.setTabOrder(self.prodname, self.externalno)
        Dialog.setTabOrder(self.externalno, self.commonname)
        Dialog.setTabOrder(self.commonname, self.allowno)
        Dialog.setTabOrder(self.allowno, self.inputcode)
        Dialog.setTabOrder(self.inputcode, self.spec)
        Dialog.setTabOrder(self.spec, self.packageLv)
        Dialog.setTabOrder(self.packageLv, self.package_2)
        Dialog.setTabOrder(self.package_2, self.checkunit)
        Dialog.setTabOrder(self.checkunit, self.acceptButton)
        Dialog.setTabOrder(self.acceptButton, self.cancelButton)
        Dialog.setTabOrder(self.cancelButton, self.precheckitem)
        Dialog.setTabOrder(self.precheckitem, self.formula)
        Dialog.setTabOrder(self.formula, self.prodcheckitem)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "物料详细信息"))
        self.groupBox_4.setTitle(_translate("Dialog", "成品生产线："))
        self.workshoplabel.setText(_translate("Dialog", "生产车间："))
        self.workshop.setText(_translate("Dialog", "..."))
        self.productionlinelabel.setText(_translate("Dialog", "生产线："))
        self.qrtype.setTitle(_translate("Dialog", "二维码采集方式："))
        self.radioButton.setText(_translate("Dialog", "正常采集"))
        self.radioButton_2.setText(_translate("Dialog", "三级包装—只扫两级码"))
        self.radioButton_3.setText(_translate("Dialog", "一级包装"))
        self.packagelabel.setText(_translate("Dialog", "包装规格："))
        self.acceptButton.setText(_translate("Dialog", "确认"))
        self.cancelButton.setText(_translate("Dialog", "取消"))
        self.medkindlabel.setText(_translate("Dialog", "剂型："))
        self.checkunitlabel.setText(_translate("Dialog", "取样单位："))
        self.idlabel.setText(_translate("Dialog", "编号："))
        self.namelabel.setText(_translate("Dialog", "商品名："))
        self.inputlabel.setText(_translate("Dialog", "输入码："))
        self.allownolabel.setText(_translate("Dialog", "批准文号："))
        self.externalnolabel.setText(_translate("Dialog", "外部编码："))
        self.kindlabel.setText(_translate("Dialog", "通用名："))
        self.speclabel.setText(_translate("Dialog", "含量规格："))
        self.packageLvlabel.setText(_translate("Dialog", "包装级别："))
        self.checkunit.setItemText(0, _translate("Dialog", "Kg（千克）"))
        self.checkunit.setItemText(1, _translate("Dialog", "g（克）"))
        self.checkunit.setItemText(2, _translate("Dialog", "L（升）"))
        self.checkunit.setItemText(3, _translate("Dialog", "ml（毫升）"))
        self.packageLv.setItemText(0, _translate("Dialog", "一级包装"))
        self.packageLv.setItemText(1, _translate("Dialog", "二级包装"))
        self.packageLv.setItemText(2, _translate("Dialog", "三级包装"))
        self.packageLv.setItemText(3, _translate("Dialog", "四级包装"))
        self.expiredlabel.setText(_translate("Dialog", "有效期："))
        self.storagelabel.setText(_translate("Dialog", "储存条件："))
        self.groupBox_3.setTitle(_translate("Dialog", "退货生产线："))
        self.bworkshoplabel.setText(_translate("Dialog", "生产车间："))
        self.bproductionlinelabel.setText(_translate("Dialog", "生产线："))
        self.bworkshop.setText(_translate("Dialog", "..."))
        self.tab.setTabText(self.tab.indexOf(self.tab_1), _translate("Dialog", "基础资料"))
        self.formula.headerItem().setText(0, _translate("Dialog", "id"))
        self.formula.headerItem().setText(1, _translate("Dialog", "类别"))
        self.formula.headerItem().setText(2, _translate("Dialog", "种类"))
        self.formula.headerItem().setText(3, _translate("Dialog", "数量"))
        self.formula.headerItem().setText(4, _translate("Dialog", "计算公式"))
        self.tab.setTabText(self.tab.indexOf(self.tab_2), _translate("Dialog", "产品配方"))
        self.precheckitem.headerItem().setText(0, _translate("Dialog", "id"))
        self.precheckitem.headerItem().setText(1, _translate("Dialog", "序号"))
        self.precheckitem.headerItem().setText(2, _translate("Dialog", "类别"))
        self.precheckitem.headerItem().setText(3, _translate("Dialog", "项目名称"))
        self.precheckitem.headerItem().setText(4, _translate("Dialog", "标准规定"))
        self.precheckitem.headerItem().setText(5, _translate("Dialog", "结果类型"))
        self.precheckitem.headerItem().setText(6, _translate("Dialog", "入库类别"))
        self.tab.setTabText(self.tab.indexOf(self.tab_3), _translate("Dialog", "中间产品检验项目"))
        self.prodcheckitem.headerItem().setText(0, _translate("Dialog", "id"))
        self.prodcheckitem.headerItem().setText(1, _translate("Dialog", "序号"))
        self.prodcheckitem.headerItem().setText(2, _translate("Dialog", "类别"))
        self.prodcheckitem.headerItem().setText(3, _translate("Dialog", "项目名称"))
        self.prodcheckitem.headerItem().setText(4, _translate("Dialog", "标准规定"))
        self.prodcheckitem.headerItem().setText(5, _translate("Dialog", "结果类型"))
        self.prodcheckitem.headerItem().setText(6, _translate("Dialog", "入库类别"))
        self.tab.setTabText(self.tab.indexOf(self.tab_4), _translate("Dialog", "成品检验项目"))
        self.samplecheckitem.headerItem().setText(0, _translate("Dialog", "id"))
        self.samplecheckitem.headerItem().setText(1, _translate("Dialog", "序号"))
        self.samplecheckitem.headerItem().setText(2, _translate("Dialog", "类别"))
        self.samplecheckitem.headerItem().setText(3, _translate("Dialog", "项目名称"))
        self.samplecheckitem.headerItem().setText(4, _translate("Dialog", "标准规定"))
        self.samplecheckitem.headerItem().setText(5, _translate("Dialog", "结果类型"))
        self.samplecheckitem.headerItem().setText(6, _translate("Dialog", "入库类别"))
        self.tab.setTabText(self.tab.indexOf(self.tab_5), _translate("Dialog", "留样检验项目"))
        self.groupBox_2.setTitle(_translate("Dialog", "标签图"))
        self.groupBox.setTitle(_translate("Dialog", "标签记录"))
        self.labellist.headerItem().setText(0, _translate("Dialog", "id"))
        self.labellist.headerItem().setText(1, _translate("Dialog", "图片名"))
        self.labellist.headerItem().setText(2, _translate("Dialog", "建立者"))
        self.labellist.headerItem().setText(3, _translate("Dialog", "建立时间"))
        self.labellist.headerItem().setText(4, _translate("Dialog", "imageid"))
        self.labelvaildButton.setText(_translate("Dialog", "生效"))
        self.labelinvaildButton.setText(_translate("Dialog", "失效"))
        self.tab.setTabText(self.tab.indexOf(self.tab_6), _translate("Dialog", "产品标签图"))
