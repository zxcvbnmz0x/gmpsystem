# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from clerks.views.deptclerksUI import Ui_clerks
from clerks.controllers.modifydeptment import ModifyDeptment
from clerks.controllers.clerkdetail import ClerkDtail
from clerks.models.deptclerkmodel import DeptClerkModel


class Clerks(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.clerks = Ui_clerks()
        self.clerks.setupUi(self)
        # 实例化查询类
        self.deptModel = DeptClerkModel()
        # 全部部门信息
        self.alldeptment = []
        # 全部人员信息
        self.allclerks = []
        # 显示在职/离职的人员，0为在职，1为离职
        self.clerks_disabled = 0
        # 把所有预定义好的信号连接到槽
        self.signal_connect_slit()

        self.show()

    def show(self):
        # 增加部门列表里的内容
        self.refresh_deptment_list()
        # 增加部门右键点击事件
        self.clerks.deptlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 部门菜单右键功能
        self.clerks.deptlist.customContextMenuRequested.connect(
            self.dept_generate_menu
        )
        # 增加人员右键点击事件
        self.clerks.userlist.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        # 部门菜单右键功能
        self.clerks.userlist.customContextMenuRequested.connect(
            self.clerk_generate_menu
        )

        # 连接数据库，获取全部人员
        self.allclerks = self.deptModel.get_all_clerks()
        # 尺寸根据内容调整
        self.clerks.userlist.sizeHintForColumn(1)
        # 增加显示部门人员功能
        self.clerks.deptlist.currentItemChanged.connect(self.change_clerks)
        # 显示人员列表
        self.adduseritem(self.clerks.userlist, *self.allclerks)

    '''
    def setGeometry(self, *__args):
        rect = QtCore.QRect(*__args)
        # self.clerks.widget.setGeometry(rect)
    '''

    def move(self, x, y):
        self.clerks.deptlist.move(x, y)
        # self.clerks.clerkslist.move(x+136, y)

    '''
    def resize(self, *__args):
        qsize = QtCore.QSize(*__args)
        # self.clerks.widget.resize(qsize)
    '''

    def adduseritem(self, parent, *items):
        self.clerks.userlist.clear()
        for item in items:
            user = QtWidgets.QTreeWidgetItem(parent)
            user.setText(0, item['pid'])
            user.setText(1, item['clerkname'])
            user.setText(2, item['sex'])
            user.setText(3, '123')
            user.setText(4, 'abc')
            user.setText(5, item['edudegree'])
            user.setText(6, item['marrystatus'])
            user.setText(7, item['idno'])
            user.setText(8, item['telno'])

    # 把所有预定义好的信号连接到槽
    def signal_connect_slit(self):
        # 绑定在职的功能
        self.clerks.incumbency.clicked.connect(
            lambda: self.set_disabled(self.clerks.incumbency)
        )
        # 绑定离职的功能
        self.clerks.severance.clicked.connect(
            lambda: self.set_disabled(self.clerks.severance)
        )
        # 绑定人员列表双击的功能
        self.clerks.userlist.itemDoubleClicked.connect(
            self.on_userlist_itemDoubleClicked
        )

    # 人员列表双击的功能
    def on_userlist_itemDoubleClicked(self,  QTreeWidgetItem, p_int):
        pid = QTreeWidgetItem.text(0)
        for item in self.allclerks.values():
            if item['pid'] == pid:
                clerkid = item['clerkid']
        #print(self.allclerks[self.clerks.userlist.currentIndex()])
        #print(self.allclerks[self.clerks.userlist.currentIndex()]['clerkid'])
        try:
            # QTreeWidgetItem.text(0)
            # clerkid = self.allclerks.index()
            clerk_detail = ClerkDtail(clerkid)
            clerk_detail.show()
            # 连接数据库，获取全部人员
            self.allclerks = self.deptModel.get_all_clerks()
            # 显示人员列表
            self.adduseritem(self.clerks.userlist, *self.allclerks)
        except Exception as e:
            print(e)
            criticaldialog = QtWidgets.QMessageBox()
            criticaldialog.setWindowTitle("提示")
            criticaldialog.setText("您没有查看人员详情的权限")
            criticaldialog.setIcon(QtWidgets.QMessageBox.Critical)
            # 添加Yes和No2个按键
            criticaldialog.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )
            # 设置按键的文本为“确认”和“取消”
            button_yes = criticaldialog.button(QtWidgets.QMessageBox.Yes)
            button_yes.setText("确认")
            button_no = criticaldialog.button(QtWidgets.QMessageBox.No)
            button_no.setText("取消")
            criticaldialog.exec_()


    # 部门菜单右键功能
    def dept_generate_menu(self, pos):
        menu = QtWidgets.QMenu()
        item1 = menu.addAction("新建部门")
        item2 = menu.addAction("修改部门")
        item3 = menu.addAction("删除部门")
        # 把坐标转换为屏幕坐标
        screenpos = self.clerks.deptlist.mapToGlobal(pos)
        # 设置菜单显示的位置,返回点击了哪个功能
        action = menu.exec(screenpos)
        # 根据点击了哪个功能绑定对应的事件

        if action == item1:
            self.new_deptment(self.clerks.deptlist)
        elif action == item2:
            self.modify_deptment(self.clerks.deptlist)
        elif action == item3:
            self.delete_deptment()
        else:
            pass

    # 部门菜单右键功能
    def clerk_generate_menu(self, pos):
        menu = QtWidgets.QMenu()
        item1 = menu.addAction("新增人员信息")
        item2 = menu.addAction("修改人员信息")
        item3 = menu.addAction("删除人员信息")
        # 把坐标转换为屏幕坐标
        screenpos = self.clerks.userlist.mapToGlobal(pos)
        # 设置菜单显示的位置,返回点击了哪个功能
        action = menu.exec(screenpos)
        # 根据点击了哪个功能绑定对应的事件

        if action == item1:
            self.new_deptment(self.clerks.deptlist)
        elif action == item2:
            self.modify_deptment(self.clerks.deptlist)
        elif action == item3:
            self.delete_deptment()
        else:
            pass

    # 新建部门，如果没有选择当前部门则默认父部门为空，否则为当前部门
    def new_deptment(self, qtree):
        # 当前部门ID和名称
        dept_id = qtree.currentItem().text(0)
        dept_name = qtree.currentItem().text(1)
        # 实例窗口对象
        new_deptment = ModifyDeptment(qtree)
        # 判断当前部门ID是否为空或者为“全部部门”
        if dept_id and dept_id != "全部部门":
            new_deptment.set_dept_list(
                dept_id + " " + dept_name, *self.alldeptment
            )
        else:
            new_deptment.set_dept_list('', *self.alldeptment)

        new_deptment.getDeptData.connect(self.accept_func)
        # 显示窗口
        new_deptment.exec_("新建部门", "确定", "取消")

    # 修改当前选择的部门，若当前未选择部门则无操作
    def modify_deptment(self, qtree):
        # 当前部门ID
        dept_id = qtree.currentItem().text(0)
        # 当前部门名称
        dept_name = qtree.currentItem().text(1)
        parent_id = ""
        parent_name = ""
        for item in self.alldeptment:
            if item['deptid'] == dept_id:
                parent_id = item['parentid']
                break
        if parent_id:
            for item in self.alldeptment:
                if item['deptid'] == parent_id:
                    parent_name = item['deptname']
                    break
        # 判断当前部门ID是否为空或者为“全部部门”
        if dept_id and dept_id != "全部部门":
            # 实例窗口对象
            modify_deptment = ModifyDeptment(qtree, dept_id, 1)

            modify_deptment.set_dept_list(
                parent_id + ' ' + parent_name, *self.alldeptment
            )

            modify_deptment.set_item('deptId', dept_id)
            modify_deptment.set_item('deptName', dept_name)

            modify_deptment.getDeptData.connect(self.update_dept)
            # 显示窗口
            modify_deptment.exec_("编辑部门", "确定", "取消")

    # 删除当前选择的部门，若当前未选择部门则无操作
    def delete_deptment(self):
        item = self.clerks.deptlist.currentItem()
        # 建立提示窗口，设置对应窗口名、图标、提示消息
        warmdialog = QtWidgets.QMessageBox()
        warmdialog.setWindowTitle("警告")
        warmdialog.setIcon(QtWidgets.QMessageBox.Warning)
        # 添加Yes和No2个按键
        warmdialog.setStandardButtons(
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        # 设置按键的文本为“确认”和“取消”
        button_yes = warmdialog.button(QtWidgets.QMessageBox.Yes)
        button_yes.setText("确认")
        button_no = warmdialog.button(QtWidgets.QMessageBox.Yes)
        button_no.setText("取消")

        if item.text(0) == "全部部门":
            return
        if item.childCount() > 0:
            warmdialog.setText("该部门下还有子部门，是否删除全部部门？")
            message = warmdialog.exec_()
            # ========================================
            # 如果按下了确认则删除当前部门和所有子部门
            # 追加判断当前部门和子部门是否有人员，待实现的功能
            # ========================================
            if message == QtWidgets.QMessageBox.Yes:
                # 获取当前部门
                current_item = self.clerks.deptlist.currentItem()
                current_dept_id = current_item.text(0)
                child_dept_set = self.foreach_childdeptment(current_dept_id)
                self.deptModel.del_deptment(*child_dept_set)
                self.refresh_deptment_list()

        else:
            warmdialog.setText("确认删除此部门？")
            message = warmdialog.exec_()
            # ========================================
            # 如果按下了确认则删除当前部门和所有子部门
            # 追加判断当前部门和子部门是否有人员，待实现的功能
            # ========================================
            if message == QtWidgets.QMessageBox.Yes:
                current_item = self.clerks.deptlist.currentItem()
                self.deptModel.del_deptment(current_item.text(0))
                self.refresh_deptment_list()

    # 新建/修改部门返回功能
    # 把结果存入数据库
    def accept_func(self, args):
        createdept = {
            'deptid': args[0], 'deptname': args[1], 'parentid': args[2],
            'inputcode': args[3], 'authority': args[4]
        }
        res = self.deptModel.create_deptment(**createdept)
        if res:
            # 刷新部门列表
            self.refresh_deptment_list()
            # 把新建立的部门设置为当前选项
            current_item = self.clerks.deptlist.findItems(
                args[0], QtCore.Qt.MatchRecursive, QtCore.Qt.MatchExactly
            )
            self.clerks.deptlist.setCurrentItem(current_item[0])

    def update_dept(self, args):
        print(args)
        updatedept = {
            'deptid': args[1], 'deptname': args[2], 'parentid': args[3],
            'inputcode': args[4], 'authority': args[5]
        }
        res = self.deptModel.update_deptment(args[0], **updatedept)

        if res:
            # 刷新部门列表
            self.refresh_deptment_list()
            # 把新建立的部门设置为当前选项
            current_item = self.clerks.deptlist.findItems(
                args[1], QtCore.Qt.MatchRecursive, QtCore.Qt.MatchExactly
            )
            self.clerks.deptlist.setCurrentItem(current_item[0])

    # 刷新部门列表的内容
    def refresh_deptment_list(self):
        # 查询所有部门信息
        self.alldeptment = self.deptModel.get_all_deptment(
            'deptid', 'deptname',  'parentid', 'authority'
        )
        # 清空“全部部门”下的所有子节点
        self.clerks.deptlist.clear()
        # 获得“全部部门”的item地址
        alldeptitem = QtWidgets.QTreeWidgetItem(self.clerks.deptlist)
        alldeptitem.setText(0, "全部部门")
        # 把全部部门作为父节点，把查询到的部门信息添加到“全部部门”下
        self.adddeptitem(self.clerks.deptlist, alldeptitem,
                         *self.alldeptment)
        # 设置“全部部门”为当前选中项目
        self.clerks.deptlist.setCurrentItem(alldeptitem)
        # 展开“所有部门”
        self.clerks.deptlist.expandItem(alldeptitem)

    # 添加部门列表的内容
    # parent  树根节点
    # aldeptitem    “全部部门”的地址，作为其他节点的父节点
    # items         需要增加的节点内容
    # 方法：首先遍历item,判断parentid是否为空，若为空，则判断deptid对应的节点
    #       是否已经被创建，若已存在则设置deptid和deptname的值，若没有被创建
    #       则建立对应的节点（父节点为alldeptitem）,并设置deptid和deptname的值
    #
    #       若parentid不为空，则把父节点设置为parentid对应的节点，若父节点还没
    #       被创建则先建立父节点并设置deptid  = parentid,用于后续查询节点用。
    def adddeptitem(self, parent, alldeptitem, *items):
        for item in items:
            # 有上级部门
            if item['parentid']:
                # 获取/建立上级部门的节点
                parent_treeitem = self.create_parent_treeitem(
                    item['parentid'], *items
                )
                childtreeitem = QtWidgets.QTreeWidgetItem(parent_treeitem)
                childtreeitem.setText(0, item["deptid"])
                childtreeitem.setText(1, item["deptname"])
            else:
                treeitem = parent.findItems(
                    item["deptid"], QtCore.Qt.MatchRecursive,
                    QtCore.Qt.MatchExactly
                )
                # 当前节点已经存在
                if treeitem:
                    treeitem[0].setText(0, item["deptid"])
                    treeitem[0].setText(1, item["deptname"])
                else:
                    childtreeitem = QtWidgets.QTreeWidgetItem(alldeptitem)
                    childtreeitem.setText(0, item["deptid"])
                    childtreeitem.setText(1, item["deptname"])

    # 添加所有部门，逐层添加上级部门，直到上级部门已经存在
    def create_parent_treeitem(self, parent_id, *items):
        for item in items:
            if parent_id == item['deptid']:
                parent_item = self.clerks.deptlist.findItems(
                    parent_id, QtCore.Qt.MatchRecursive, QtCore.Qt.MatchExactly
                )
                # 存在上级节点
                if parent_item:
                    return parent_item[0]
                # 不存在上级节点，且祖父节点不为空
                elif item['parentid']:
                    grand_item = self.create_parent_treeitem(
                        item['parentid'], *items
                    )
                    parent = QtWidgets.QTreeWidgetItem(grand_item)
                    parent.setText(0, item['parentid'])
                    return parent
                # 不存在上级节点，且祖父节点为空
                else:
                    alldept = self.clerks.deptlist.findItems(
                        "全部部门", QtCore.Qt.MatchRecursive,
                        QtCore.Qt.MatchExactly
                    )
                    parent = QtWidgets.QTreeWidgetItem(alldept[0])
                    parent.setText(0, parent_id)
                    return parent

    # 遍历当前部门的子部门，并放回子部门的列表
    def foreach_childdeptment(self, deptment_id):
        deptment_list = set()
        for item in self.alldeptment:
            if item['parentid'] == deptment_id:
                deptment_list.add(item['deptid'])
                grand_deptment = self.foreach_childdeptment(item['deptid'])
                if grand_deptment:
                    deptment_list.update(grand_deptment)
        return deptment_list

    # 当前部门改变，刷新人员列表
    def change_clerks(self, qtreeitem):
        current_item = qtreeitem.text(0)
        if current_item == "全部部门":
            self.allclerks = self.deptModel.get_all_clerks("",
                                                           self.clerks_disabled)
            self.adduseritem(self.clerks.userlist, *self.allclerks)
        else:
            print(self.clerks_disabled)
            self.allclerks = self.deptModel.get_all_clerks(current_item,
                                                           self.clerks_disabled)
            self.adduseritem(self.clerks.userlist, *self.allclerks)

    def set_disabled(self, widget):
        button_objname = widget.objectName()
        if button_objname == "severance":
            self.clerks_disabled = 1
            widget.setDisabled(True)
            self.clerks.incumbency.setDisabled(False)
        else:
            self.clerks_disabled = 0
            widget.setDisabled(True)
            self.clerks.severance.setDisabled(False)
        qtreeitem = self.clerks.deptlist.currentItem()
        self.change_clerks(qtreeitem)
