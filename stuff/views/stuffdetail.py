# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'stuffdetail.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(640, 520)
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
        self.checkunit = QtWidgets.QComboBox(self.tab_1)
        self.checkunit.setEditable(False)
        self.checkunit.setObjectName("checkunit")
        self.checkunit.addItem("")
        self.checkunit.addItem("")
        self.checkunit.addItem("")
        self.checkunit.addItem("")
        self.gridLayout_6.addWidget(self.checkunit, 2, 4, 1, 1)
        self.checkunitlabel = QtWidgets.QLabel(self.tab_1)
        self.checkunitlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.checkunitlabel.setObjectName("checkunitlabel")
        self.gridLayout_6.addWidget(self.checkunitlabel, 2, 3, 1, 1)
        self.idlabel = QtWidgets.QLabel(self.tab_1)
        self.idlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.idlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.idlabel.setObjectName("idlabel")
        self.gridLayout_6.addWidget(self.idlabel, 1, 1, 1, 1)
        self.typelabel = QtWidgets.QLabel(self.tab_1)
        self.typelabel.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.typelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.typelabel.setObjectName("typelabel")
        self.gridLayout_6.addWidget(self.typelabel, 0, 1, 1, 1)
        self.namelabel = QtWidgets.QLabel(self.tab_1)
        self.namelabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.namelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.namelabel.setObjectName("namelabel")
        self.gridLayout_6.addWidget(self.namelabel, 2, 1, 1, 1)
        self.workshoplabel = QtWidgets.QLabel(self.tab_1)
        self.workshoplabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.workshoplabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.workshoplabel.setObjectName("workshoplabel")
        self.gridLayout_6.addWidget(self.workshoplabel, 10, 1, 1, 1)
        self.externalnolabel = QtWidgets.QLabel(self.tab_1)
        self.externalnolabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.externalnolabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.externalnolabel.setObjectName("externalnolabel")
        self.gridLayout_6.addWidget(self.externalnolabel, 3, 1, 1, 1)
        self.kindlabel = QtWidgets.QLabel(self.tab_1)
        self.kindlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.kindlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.kindlabel.setObjectName("kindlabel")
        self.gridLayout_6.addWidget(self.kindlabel, 4, 1, 1, 1)
        self.purchasingunitlabel = QtWidgets.QLabel(self.tab_1)
        self.purchasingunitlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.purchasingunitlabel.setObjectName("purchasingunitlabel")
        self.gridLayout_6.addWidget(self.purchasingunitlabel, 1, 3, 1, 1)
        self.expired = QtWidgets.QLineEdit(self.tab_1)
        self.expired.setObjectName("expired")
        self.gridLayout_6.addWidget(self.expired, 6, 4, 1, 1)
        self.ceffectunit = QtWidgets.QLineEdit(self.tab_1)
        self.ceffectunit.setObjectName("ceffectunit")
        self.gridLayout_6.addWidget(self.ceffectunit, 7, 4, 1, 1)
        self.stuffname = QtWidgets.QLineEdit(self.tab_1)
        self.stuffname.setObjectName("stuffname")
        self.gridLayout_6.addWidget(self.stuffname, 2, 2, 1, 1)
        self.recheck = QtWidgets.QLineEdit(self.tab_1)
        self.recheck.setObjectName("recheck")
        self.gridLayout_6.addWidget(self.recheck, 5, 4, 1, 1)
        self.lowlimit = QtWidgets.QLineEdit(self.tab_1)
        self.lowlimit.setObjectName("lowlimit")
        self.gridLayout_6.addWidget(self.lowlimit, 4, 4, 1, 1)
        self.upperlimit = QtWidgets.QLineEdit(self.tab_1)
        self.upperlimit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.upperlimit.setInputMask("")
        self.upperlimit.setClearButtonEnabled(False)
        self.upperlimit.setObjectName("upperlimit")
        self.gridLayout_6.addWidget(self.upperlimit, 3, 4, 1, 1)
        self.kind = QtWidgets.QLineEdit(self.tab_1)
        self.kind.setObjectName("kind")
        self.gridLayout_6.addWidget(self.kind, 4, 2, 1, 1)
        self.externalno = QtWidgets.QLineEdit(self.tab_1)
        self.externalno.setObjectName("externalno")
        self.gridLayout_6.addWidget(self.externalno, 3, 2, 1, 1)
        self.stuffid = QtWidgets.QLineEdit(self.tab_1)
        self.stuffid.setObjectName("stuffid")
        self.gridLayout_6.addWidget(self.stuffid, 1, 2, 1, 1)
        self.lowlimitlabel = QtWidgets.QLabel(self.tab_1)
        self.lowlimitlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lowlimitlabel.setObjectName("lowlimitlabel")
        self.gridLayout_6.addWidget(self.lowlimitlabel, 3, 3, 1, 1)
        self.upperlimitlabel = QtWidgets.QLabel(self.tab_1)
        self.upperlimitlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.upperlimitlabel.setObjectName("upperlimitlabel")
        self.gridLayout_6.addWidget(self.upperlimitlabel, 4, 3, 1, 1)
        self.rechecklabel = QtWidgets.QLabel(self.tab_1)
        self.rechecklabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.rechecklabel.setObjectName("rechecklabel")
        self.gridLayout_6.addWidget(self.rechecklabel, 5, 3, 1, 1)
        self.expiredlabel = QtWidgets.QLabel(self.tab_1)
        self.expiredlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.expiredlabel.setObjectName("expiredlabel")
        self.gridLayout_6.addWidget(self.expiredlabel, 6, 3, 1, 1)
        self.purchasingunit = QtWidgets.QComboBox(self.tab_1)
        self.purchasingunit.setObjectName("purchasingunit")
        self.purchasingunit.addItem("")
        self.purchasingunit.addItem("")
        self.purchasingunit.addItem("")
        self.purchasingunit.addItem("")
        self.gridLayout_6.addWidget(self.purchasingunit, 1, 4, 1, 1)
        self.stufftype = QtWidgets.QComboBox(self.tab_1)
        self.stufftype.setObjectName("stufftype")
        self.stufftype.addItem("")
        self.stufftype.addItem("")
        self.stufftype.addItem("")
        self.stufftype.addItem("")
        self.stufftype.addItem("")
        self.gridLayout_6.addWidget(self.stufftype, 0, 2, 1, 1)
        self.productionlinelabel = QtWidgets.QLabel(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.productionlinelabel.sizePolicy().hasHeightForWidth())
        self.productionlinelabel.setSizePolicy(sizePolicy)
        self.productionlinelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.productionlinelabel.setObjectName("productionlinelabel")
        self.gridLayout_6.addWidget(self.productionlinelabel, 11, 1, 1, 1)
        self.productionline = QtWidgets.QLabel(self.tab_1)
        self.productionline.setText("")
        self.productionline.setObjectName("productionline")
        self.gridLayout_6.addWidget(self.productionline, 11, 2, 1, 1)
        self.cancelButton = QtWidgets.QPushButton(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cancelButton.sizePolicy().hasHeightForWidth())
        self.cancelButton.setSizePolicy(sizePolicy)
        self.cancelButton.setObjectName("cancelButton")
        self.gridLayout_6.addWidget(self.cancelButton, 12, 4, 1, 1)
        self.acceptButton = QtWidgets.QPushButton(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acceptButton.sizePolicy().hasHeightForWidth())
        self.acceptButton.setSizePolicy(sizePolicy)
        self.acceptButton.setObjectName("acceptButton")
        self.gridLayout_6.addWidget(self.acceptButton, 12, 3, 1, 1)
        self.ceffectunitlabel = QtWidgets.QLabel(self.tab_1)
        self.ceffectunitlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.ceffectunitlabel.setObjectName("ceffectunitlabel")
        self.gridLayout_6.addWidget(self.ceffectunitlabel, 7, 3, 1, 1)
        self.storage = QtWidgets.QLineEdit(self.tab_1)
        self.storage.setObjectName("storage")
        self.gridLayout_6.addWidget(self.storage, 9, 4, 1, 1)
        self.storagelabel = QtWidgets.QLabel(self.tab_1)
        self.storagelabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.storagelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.storagelabel.setObjectName("storagelabel")
        self.gridLayout_6.addWidget(self.storagelabel, 9, 3, 1, 1)
        self.packagelabel = QtWidgets.QLabel(self.tab_1)
        self.packagelabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.packagelabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.packagelabel.setObjectName("packagelabel")
        self.gridLayout_6.addWidget(self.packagelabel, 9, 1, 1, 1)
        self.package_2 = QtWidgets.QLineEdit(self.tab_1)
        self.package_2.setObjectName("package_2")
        self.gridLayout_6.addWidget(self.package_2, 9, 2, 1, 1)
        self.packageLv = QtWidgets.QComboBox(self.tab_1)
        self.packageLv.setObjectName("packageLv")
        self.packageLv.addItem("")
        self.packageLv.addItem("")
        self.packageLv.addItem("")
        self.packageLv.addItem("")
        self.gridLayout_6.addWidget(self.packageLv, 8, 2, 1, 1)
        self.packageLvlabel = QtWidgets.QLabel(self.tab_1)
        self.packageLvlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.packageLvlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.packageLvlabel.setObjectName("packageLvlabel")
        self.gridLayout_6.addWidget(self.packageLvlabel, 8, 1, 1, 1)
        self.speclabel = QtWidgets.QLabel(self.tab_1)
        self.speclabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.speclabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.speclabel.setObjectName("speclabel")
        self.gridLayout_6.addWidget(self.speclabel, 7, 1, 1, 1)
        self.spec = QtWidgets.QLineEdit(self.tab_1)
        self.spec.setObjectName("spec")
        self.gridLayout_6.addWidget(self.spec, 7, 2, 1, 1)
        self.inputlabel = QtWidgets.QLabel(self.tab_1)
        self.inputlabel.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.inputlabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.inputlabel.setObjectName("inputlabel")
        self.gridLayout_6.addWidget(self.inputlabel, 6, 1, 1, 1)
        self.inputcode = QtWidgets.QLineEdit(self.tab_1)
        self.inputcode.setObjectName("inputcode")
        self.gridLayout_6.addWidget(self.inputcode, 6, 2, 1, 1)
        self.allownolabel = QtWidgets.QLabel(self.tab_1)
        self.allownolabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.allownolabel.setObjectName("allownolabel")
        self.gridLayout_6.addWidget(self.allownolabel, 5, 1, 1, 1)
        self.allowno = QtWidgets.QLineEdit(self.tab_1)
        self.allowno.setObjectName("allowno")
        self.gridLayout_6.addWidget(self.allowno, 5, 2, 1, 1)
        self.workshop = QtWidgets.QToolButton(self.tab_1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.workshop.sizePolicy().hasHeightForWidth())
        self.workshop.setSizePolicy(sizePolicy)
        self.workshop.setObjectName("workshop")
        self.gridLayout_6.addWidget(self.workshop, 10, 2, 1, 1)
        self.tab.addTab(self.tab_1, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.checkitem = QtWidgets.QTreeWidget(self.tab_2)
        self.checkitem.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.checkitem.setObjectName("checkitem")
        self.gridLayout_4.addWidget(self.checkitem, 0, 0, 1, 1)
        self.tab.addTab(self.tab_2, "")
        self.tab_3 = QtWidgets.QWidget()
        self.tab_3.setObjectName("tab_3")
        self.gridLayout_5 = QtWidgets.QGridLayout(self.tab_3)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.formula = QtWidgets.QTreeWidget(self.tab_3)
        self.formula.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.formula.setObjectName("formula")
        self.gridLayout_5.addWidget(self.formula, 0, 0, 1, 1)
        self.tab.addTab(self.tab_3, "")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_4)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.precheckitem = QtWidgets.QTreeWidget(self.tab_4)
        self.precheckitem.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.precheckitem.setObjectName("precheckitem")
        self.gridLayout_3.addWidget(self.precheckitem, 0, 0, 1, 1)
        self.tab.addTab(self.tab_4, "")
        self.tab_5 = QtWidgets.QWidget()
        self.tab_5.setObjectName("tab_5")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab_5)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pdandsp = QtWidgets.QTreeWidget(self.tab_5)
        self.pdandsp.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.pdandsp.setObjectName("pdandsp")
        self.gridLayout_2.addWidget(self.pdandsp, 0, 0, 1, 1)
        self.tab.addTab(self.tab_5, "")
        self.gridLayout.addWidget(self.tab, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tab.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.stufftype, self.stuffid)
        Dialog.setTabOrder(self.stuffid, self.stuffname)
        Dialog.setTabOrder(self.stuffname, self.externalno)
        Dialog.setTabOrder(self.externalno, self.kind)
        Dialog.setTabOrder(self.kind, self.allowno)
        Dialog.setTabOrder(self.allowno, self.inputcode)
        Dialog.setTabOrder(self.inputcode, self.spec)
        Dialog.setTabOrder(self.spec, self.packageLv)
        Dialog.setTabOrder(self.packageLv, self.package_2)
        Dialog.setTabOrder(self.package_2, self.purchasingunit)
        Dialog.setTabOrder(self.purchasingunit, self.checkunit)
        Dialog.setTabOrder(self.checkunit, self.upperlimit)
        Dialog.setTabOrder(self.upperlimit, self.lowlimit)
        Dialog.setTabOrder(self.lowlimit, self.recheck)
        Dialog.setTabOrder(self.recheck, self.expired)
        Dialog.setTabOrder(self.expired, self.ceffectunit)
        Dialog.setTabOrder(self.ceffectunit, self.storage)
        Dialog.setTabOrder(self.storage, self.workshop)
        Dialog.setTabOrder(self.workshop, self.acceptButton)
        Dialog.setTabOrder(self.acceptButton, self.cancelButton)
        Dialog.setTabOrder(self.cancelButton, self.tab)
        Dialog.setTabOrder(self.tab, self.checkitem)
        Dialog.setTabOrder(self.checkitem, self.formula)
        Dialog.setTabOrder(self.formula, self.precheckitem)
        Dialog.setTabOrder(self.precheckitem, self.pdandsp)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "物料详细信息"))
        self.checkunit.setItemText(0, _translate("Dialog", "Kg（千克）"))
        self.checkunit.setItemText(1, _translate("Dialog", "g（克）"))
        self.checkunit.setItemText(2, _translate("Dialog", "L（升）"))
        self.checkunit.setItemText(3, _translate("Dialog", "ml（毫升）"))
        self.checkunitlabel.setText(_translate("Dialog", "取样单位："))
        self.idlabel.setText(_translate("Dialog", "编号："))
        self.typelabel.setText(_translate("Dialog", "物料类别："))
        self.namelabel.setText(_translate("Dialog", "名称："))
        self.workshoplabel.setText(_translate("Dialog", "生产车间："))
        self.externalnolabel.setText(_translate("Dialog", "外部编码："))
        self.kindlabel.setText(_translate("Dialog", "种类："))
        self.purchasingunitlabel.setText(_translate("Dialog", "入库单位："))
        self.lowlimitlabel.setText(_translate("Dialog", "库存上限："))
        self.upperlimitlabel.setText(_translate("Dialog", "库存下限："))
        self.rechecklabel.setText(_translate("Dialog", "复检天数："))
        self.expiredlabel.setText(_translate("Dialog", "有效期："))
        self.purchasingunit.setItemText(0, _translate("Dialog", "Kg（千克）"))
        self.purchasingunit.setItemText(1, _translate("Dialog", "g（克）"))
        self.purchasingunit.setItemText(2, _translate("Dialog", "L（升）"))
        self.purchasingunit.setItemText(3, _translate("Dialog", "ml（毫升）"))
        self.stufftype.setItemText(0, _translate("Dialog", "主材料"))
        self.stufftype.setItemText(1, _translate("Dialog", "前处理材料"))
        self.stufftype.setItemText(2, _translate("Dialog", "辅材料"))
        self.stufftype.setItemText(3, _translate("Dialog", "内包材"))
        self.stufftype.setItemText(4, _translate("Dialog", "外包材"))
        self.productionlinelabel.setText(_translate("Dialog", "生产线："))
        self.cancelButton.setText(_translate("Dialog", "取消"))
        self.acceptButton.setText(_translate("Dialog", "确认"))
        self.ceffectunitlabel.setText(_translate("Dialog", "含量单位："))
        self.storagelabel.setText(_translate("Dialog", "储存条件："))
        self.packagelabel.setText(_translate("Dialog", "包装规格："))
        self.packageLv.setItemText(0, _translate("Dialog", "一级包装"))
        self.packageLv.setItemText(1, _translate("Dialog", "二级包装"))
        self.packageLv.setItemText(2, _translate("Dialog", "三级包装"))
        self.packageLv.setItemText(3, _translate("Dialog", "四级包装"))
        self.packageLvlabel.setText(_translate("Dialog", "包装级别："))
        self.speclabel.setText(_translate("Dialog", "含量规格："))
        self.inputlabel.setText(_translate("Dialog", "输入码："))
        self.allownolabel.setText(_translate("Dialog", "批准文号："))
        self.workshop.setText(_translate("Dialog", "..."))
        self.tab.setTabText(self.tab.indexOf(self.tab_1), _translate("Dialog", "基础资料"))
        self.checkitem.headerItem().setText(0, _translate("Dialog", "id"))
        self.checkitem.headerItem().setText(1, _translate("Dialog", "序号"))
        self.checkitem.headerItem().setText(2, _translate("Dialog", "类别"))
        self.checkitem.headerItem().setText(3, _translate("Dialog", "项目名称"))
        self.checkitem.headerItem().setText(4, _translate("Dialog", "标准规定"))
        self.checkitem.headerItem().setText(5, _translate("Dialog", "结果类型"))
        self.checkitem.headerItem().setText(6, _translate("Dialog", "入库类别"))
        self.tab.setTabText(self.tab.indexOf(self.tab_2), _translate("Dialog", "原料检验项目"))
        self.formula.headerItem().setText(0, _translate("Dialog", "id"))
        self.formula.headerItem().setText(1, _translate("Dialog", "类别"))
        self.formula.headerItem().setText(2, _translate("Dialog", "种类"))
        self.formula.headerItem().setText(3, _translate("Dialog", "数量"))
        self.formula.headerItem().setText(4, _translate("Dialog", "计算公式"))
        self.tab.setTabText(self.tab.indexOf(self.tab_3), _translate("Dialog", "前处理配方"))
        self.precheckitem.headerItem().setText(0, _translate("Dialog", "id"))
        self.precheckitem.headerItem().setText(1, _translate("Dialog", "序号"))
        self.precheckitem.headerItem().setText(2, _translate("Dialog", "类别"))
        self.precheckitem.headerItem().setText(3, _translate("Dialog", "项目名称"))
        self.precheckitem.headerItem().setText(4, _translate("Dialog", "标准规定"))
        self.precheckitem.headerItem().setText(5, _translate("Dialog", "结果类型"))
        self.precheckitem.headerItem().setText(6, _translate("Dialog", "入库类别"))
        self.tab.setTabText(self.tab.indexOf(self.tab_4), _translate("Dialog", "前处理检验项目"))
        self.pdandsp.headerItem().setText(0, _translate("Dialog", "id"))
        self.pdandsp.headerItem().setText(1, _translate("Dialog", "供应商编号"))
        self.pdandsp.headerItem().setText(2, _translate("Dialog", "供应商名称"))
        self.pdandsp.headerItem().setText(3, _translate("Dialog", "生产厂家"))
        self.tab.setTabText(self.tab.indexOf(self.tab_5), _translate("Dialog", "供应商和生产厂家"))
