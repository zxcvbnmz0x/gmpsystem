from PyQt5 import QtWidgets, QtCore, QtGui
from db.dbhelper import DbHelper
from lib.mywidget.mylineedit import myLineEdit


class mySignEdit(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        _translate = QtCore.QCoreApplication.translate

        self.username = myLineEdit(parent)
        self.username.setObjectName("username")

        self.password = QtWidgets.QLineEdit(parent)
        self.password.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password.setObjectName("password")

        self.usernamelist = QtWidgets.QTreeWidget(parent)
        self.usernamelist.headerItem().setText(0,
                                               _translate("MainWindow", "编号"))
        self.usernamelist.headerItem().setText(1,
                                               _translate("MainWindow", "编号"))
        self.username.setObjectName("usernamelist")
        self.usernamelist.setVisible(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.usernamelist.setFont(font)
        self.usernamelist.setStyleSheet("background-color: rgb(255, 255, 125);")
        self.usernamelist.setTabKeyNavigation(True)
        self.usernamelist.setIndentation(20)
        self.usernamelist.setRootIsDecorated(False)
        self.usernamelist.setUniformRowHeights(False)
        self.usernamelist.setItemsExpandable(True)
        self.usernamelist.setAnimated(False)
        self.usernamelist.setAllColumnsShowFocus(False)
        self.usernamelist.setWordWrap(False)
        self.usernamelist.setHeaderHidden(False)
        self.usernamelist.setExpandsOnDoubleClick(True)
        self.usernamelist.setObjectName("usernamelist")
        self.usernamelist.header().setVisible(True)

        self.username.textChanged.connect(self.userChanged)
        self.username.sendmsg.connect(self.inputreject)
        self.usernamelist.itemClicked.connect(self.setusername)
        self.username.returnPressed.connect(self.setusername)

    def setText(self, text):
        self.username.setText(text)

    def raise_(self):
        self.username.raise_()
        self.usernamelist.raise_()

    def setGeometry(self, *__args):
        rect = QtCore.QRect(*__args)
        self.username.setGeometry(rect)
        self.password.setGeometry(rect.x(), rect.y() + 30, rect.width(),
                                  rect.height())
        self.usernamelist.move(rect.x(), rect.y() + 20)

    def inputreject(self, e):
        self.usernamelist.keyPressEvent(e)

    def setusername(self):
        try:
            userid = self.usernamelist.currentItem().text(0)
            username = self.usernamelist.currentItem().text(1)
            self.username.setText(userid + ' ' + username)
        except:
            pass

    def userChanged(self):
        db = DbHelper()
        content = '%' + self.username.text() + '%'
        res = db.checkusername(content)
        if (res):
            self.usernamelist.clear()
            self.usernamelist.setVisible(True)
            self.usernamelist.setStyleSheet(
                "background-color: rgb(255, 255, 125)")
            for key, item in enumerate(res):
                user = QtWidgets.QTreeWidgetItem(self.usernamelist)
                user.setText(0, item['pid'])
                user.setText(1, item['clerkname'])
                if key == 0:
                    self.usernamelist.setCurrentItem(user)
            self.it = QtWidgets.QTreeWidgetItemIterator(self.usernamelist)

        else:
            self.usernamelist.setVisible(False)
            self.usernamelist.setStyleSheet(
                "background-color: rgb(255, 255, 255)")
