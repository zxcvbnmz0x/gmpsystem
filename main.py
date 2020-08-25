import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from hashlib import md5
from functools import partial

from  menu.controllers.menu import Menu

import userlogin

#确认按键，判断用户名和密码是否匹配
def enterButton():
    try:
        usernameid = ui.username.username.text().split(' ')[0]
        usernameidlist = ui.username.usernamelist.currentItem().text(0)
        print(usernameid, usernameidlist)
        if usernameid != usernameidlist and ui.username.usernamelist.isVisible():
            usernameid = usernameidlist
        print(usernameid,usernameidlist)
        password = ui.username.password.text()
        md = md5()
        md.update(password.encode(encoding='utf-8'))
        token = md.hexdigest()
        db = DbHelper()
        res = db.checkpassword(usernameid, token)
        if (res):
            ui.tips.setVisible(False)
            menu = Menu()
            menu.show(MainWindow)
        else:
            ui.tips.setVisible(True)
    except:
        ui.tips.setVisible(True)

#取消按键，用户名和密码设置为空
def cancelButton():
    ui.username.username.clear()
    ui.username.password.clear()
    ui.username.usernamelist.setVisible(False)

#根据用户列表的值设置当前的用户名，背景色设置为黄色
def setUsername(self):
    item = self.currentItem()
    ui.username.setText(item.text(0) + ' ' + item.text(1))
    ui.username.setStyleSheet("background-color: rgb(255, 255, 125)")
    self.setVisible(False)

def keyPressEvent(self,event):
    print("按下：" + str(event.key()))


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = userlogin.Ui_MainWindow()
    ui.setupUi(MainWindow)

    ui.tips.setVisible(False)
    MainWindow.show()

    #确认功能
    ui.enter.pressed.connect(enterButton)
    ui.enter.setAutoDefault(True)

    ui.cancel.clicked.connect(cancelButton)

    sys.exit(app.exec_())

