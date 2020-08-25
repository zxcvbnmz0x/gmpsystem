from PyQt5 import QtCore, QtGui, QtWidgets
from lib.utils.inputcode import Inputcode

from clerks.views.modifydeptmentUI import Ui_Dialog


class ModifyDeptment(QtCore.QObject, Ui_Dialog):
    # 自定义信号，用于传递部门编号，部门名称，上级部门Id，部门权限
    getDeptData = QtCore.pyqtSignal(list)

    def __init__(self, qtree="", dept_id=0, flag=0):
        super().__init__()
        # 当前选择的部门Qtreeitem
        self.Qtree = qtree
        # 窗口标记，0为新建部门，1为修改部门
        self.flag = flag
        # 原始部门id,仅修改部门时有用
        self.origin_id = dept_id
        self.dialog = QtWidgets.QDialog()
        # 初始化对话框
        self.setupUi(self.dialog)
        # 全部部门信息
        self.deptments = []
        # 存放填写的部门信息
        self.dept_data = {}
        # 输入码关联部门名称
        self.deptName.textChanged.connect(self.inputcode_change)
        # 把填写的内容都存入dept_data
        self.deptId.textChanged.connect(lambda: self.save_data(self.deptId))
        self.deptName.textChanged.connect(lambda: self.save_data(self.deptName))
        self.parentName.currentTextChanged.connect(
            lambda: self.save_data(self.parentName)
        )
        self.inputCode.textChanged.connect(
            lambda: self.save_data(self.inputCode)
        )
        # 点击确认功能
        self.accept.clicked.connect(self.accept_clicked)
        # 点击取消功能
        self.cancel.clicked.connect(self.cancel_clicked)
        # 隐藏提示消息
        self.deptIdtips.setVisible(False)
        self.deptNametips.setVisible(False)
        self.parentNametips.setVisible(False)

    # 显示对话框
    # tittle    对话框的标题名
    # accept    确认按键的显示内容
    # cancel    取消按键的显示内容
    def exec_(self, title="编辑部门资料", accept="确定", cancel="取消"):
        # 设置对话框标题、确认和取消按键的显示内容
        self.dialog.setWindowTitle(title)
        self.accept.setText(accept)
        self.cancel.setText(cancel)
        # 显示对话框
        self.dialog.exec_()

    # 确认功能
    def accept_clicked(self):
        # deptId:部门id
        # deptName：部门名称
        # parentId：上级部门id
        # parentName：上级部门名称
        # inputCode：快速输入码
        # authority：部门权限
        dept_id = self.deptId.text()
        dept_name = self.deptName.text()
        inputcode = self.inputCode.text()
        authority = self.get_authority()
        parent = self.parentName.currentText().split(" ")
        parent_id = ""
        parent_name = ""
        # 如果parent有2个元素则分别赋值给parentId和parentName
        if len(parent) == 2:
            parent_id = parent[0]
            parent_name = parent[1]
        # 只有一个元素，则赋值给parentName,parentId为空
        elif len(parent) == 1:
            parent_id = ""
            parent_name = parent[0]

        if self.flag == 0:
            # 新建部门
            if not dept_id:
                # 提示部门id不能为空
                self.deptIdtips.setVisible(True)
            else:
                self.deptIdtips.setVisible(False)
            if not dept_name:
                # 提示部门名称不能为空
                self.deptNametips.setVisible(True)
            else:
                self.deptNametips.setVisible(False)
            # 部门id提醒和部门名称提醒中任意一个为显示状态则提前结束函数
            if self.deptIdtips.isVisible() or self.deptNametips.isVisible():
                return
            status = 0
            parent_id_list = []
            # 判断部门id是否重复
            for item in self.deptments:
                # 部门编号重复，修改提示信息内容
                if dept_id == item['deptid']:
                    # 修改部门Id的提示内容
                    self.deptIdtips.setText("该编号已被使用")
                    self.deptIdtips.setVisible(True)
                    return
                # 判断上级部门是否存在，若找到同名的，把status设置为1
                if not parent_id and parent_name == item['deptname']:
                    parent_id_list.append(item['deptid'])
                    status = 2
                elif parent_id == item['deptid'] and \
                        parent_name == item['deptname']:
                    status = 1
            if not self.parentName.currentText():
                status = 3
            # status = 0，上级部门不为空，但找不到匹配的上级部门，提示错误消息
            # status = 1,能找到对应唯一的上级部门，返回填写的信息
            # status = 2,部门名字有重复的情况，无法确定使用那个id，弹出选择对话框
            # status = 3,上级部门为空，返回填写的信息
            if parent_id and parent_name:
                # 上级部门id和部门名称都有值，且能找到对应的部门
                if status == 1:
                    self.getDeptData.emit(
                        [dept_id, dept_name, parent_id, inputcode, authority]
                    )
                    self.dialog.accept()
                # 部门id和部门名称都有值，但没有找到对应的部门
                elif status == 0:
                    # 提示“不存在该上级部门”
                    self.parentNametips.setVisible(True)
                    return
            # 如果上级部门的编号为空，且部门编号列表长度大于1
            # 则选择的部门名称有重名的情况
            # 弹出提示，用户选择合适的部门
            elif len(parent_id_list) > 1:
                warmdialog = QtWidgets.QMessageBox()
                warmdialog.setWindowTitle("请选择合适的部门")
                warmdialog.setIcon(QtWidgets.QMessageBox.Warning)
                warmdialog.setText("你选择的上级部门存在重复的情况，请指定正确的部门。")
                # 添加Yes和No2个按键
                warmdialog.setStandardButtons(
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                # 设置按键的文本为“确认”和“取消”
                button_yes = warmdialog.button(QtWidgets.QMessageBox.Yes)
                button_yes.setText("确认")
                button_no = warmdialog.button(QtWidgets.QMessageBox.Yes)
                button_no.setText("取消")
                butoongroup = QtWidgets.QCheckBox()
                butoongroup.setText("                                      ")
                combobox = QtWidgets.QComboBox(butoongroup)
                warmdialog.setCheckBox(butoongroup)
                for i in range(len(parent_id_list)):
                    combobox.addItem(parent_id_list[i] + " " + parent_name)
                message = warmdialog.exec_()
                if message == QtWidgets.QMessageBox.Yes:
                    # 把当前选择的部门添加到上级部门中
                    self.parentName.setCurrentText(combobox.currentText())
                    self.accept_clicked()
                    return
            # 没有设置上级部门
            elif status == 3:
                dept_date = [self.origin_id, dept_id, dept_name, parent_id,
                             inputcode, authority
                             ]
                self.getDeptData.emit(dept_date)
                self.dialog.accept()
        # if修改部门
        elif self.flag == 1:
            # self.origin_id:原始的部门id
            # dept_id:修改后的部门id
            # 编号没有改
            if self.origin_id != dept_id:
                deptid_is_exist = self.check_deptid_exist()
                if deptid_is_exist == 1:
                    self.deptIdtips.setText("该编号已被使用")
                    self.deptIdtips.setVisible(True)

            parent_is_exist, parent_id_list = self.check_parent_exist()
            if parent_is_exist == 2:
                warmdialog = QtWidgets.QMessageBox()
                warmdialog.setWindowTitle("请选择合适的部门")
                warmdialog.setIcon(QtWidgets.QMessageBox.Warning)
                warmdialog.setText("你选择的上级部门存在重复的情况，"
                                   "请指定正确的部门。")
                # 添加Yes和No2个按键
                warmdialog.setStandardButtons(
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                # 设置按键的文本为“确认”和“取消”
                button_yes = warmdialog.button(QtWidgets.QMessageBox.Yes)
                button_yes.setText("确认")
                button_no = warmdialog.button(QtWidgets.QMessageBox.Yes)
                button_no.setText("取消")
                butoongroup = QtWidgets.QCheckBox()
                butoongroup.setText("                                      ")
                combobox = QtWidgets.QComboBox(butoongroup)
                warmdialog.setCheckBox(butoongroup)
                for i in range(len(parent_id_list)):
                    combobox.addItem(
                        parent_id_list[i][0] + " " + parent_id_list[i][1]
                    )
                message = warmdialog.exec_()
                if message == QtWidgets.QMessageBox.Yes:
                    # 把当前选择的部门添加到上级部门中
                    self.parentName.setCurrentText(combobox.currentText())
                    self.accept_clicked()
                    return
            dept_date = [self.origin_id, dept_id, dept_name, parent_id,
                         inputcode, authority
                         ]
            self.getDeptData.emit(dept_date)
            self.dialog.accept()

    # 检查部门编号是否存在
    def check_deptid_exist(self):
        # 存在当前部门返回1，不存在返回-1
        dept_id = self.deptId.text()
        for item in self.deptments:
            if dept_id == item['deptid']:
                return 1
        return -1

    # 检查上级部门是否符合规定
    def check_parent_exist(self):
        # 返回2个参数，
        # 参数1：存在一个上级部门返回1，不存在返回-1，
        #       存在多个上级部门（仅无parent_id时可能出现）返回2
        # 参数2：上级部门的id和名称,不存在则返回空，
        #        存在则返回[[deptid,deptname],[deptid,deptname]]
        parent = self.parentName.currentText().split(" ")
        parent_id = ""
        parent_name = ""
        if parent:
            # 如果parent有2个元素则分别赋值给parentId和parentName
            if len(parent) == 2:
                parent_id = parent[0]
                parent_name = parent[1]
            # 只有一个元素，则赋值给parentName,parentId为空
            elif len(parent) == 1:
                parent_name = parent[0]
        else:
            return -1, ''
        parent_list = []
        if parent_id:
            for item in self.deptments:
                if parent_id == item['deptid'] and \
                        parent_name == item['deptname']:
                    parent_list.append([item['deptid'], item['deptname']])
                    break
        else:
            for item in self.deptments:
                if parent_name == item['deptname']:
                    parent_list.append([item['deptid'], item['deptname']])
        if len(parent_list) > 1:
            return 2, parent_list
        else:
            return 1, parent_list

    # 取消功能
    def cancel_clicked(self):
        self.dialog.close()

    # parentname:上级部门当前选择的部门名称,默认为空
    # args:全部部门列表
    def set_dept_list(self, parentname="", *args):
        self.deptments = args
        for item in args:
            self.parentName.addItem(item['deptid'] + " " + item['deptname'])
        self.parentName.setCurrentText(parentname)

    # 输入码动态关联部门名称
    def inputcode_change(self, qstr):
        self.inputCode.setText(Inputcode.make_inputcode(qstr))

    def set_item(self, itemname, itemvalue):
        getattr(self, itemname).setText(itemvalue)

    # 取得部门权限
    # 行政    仓库  销售    设备    采购    生产  质量  财务
    #   0       0      0      0       0       0      0    0
    # 把结果拼接成字符串返回
    def get_authority(self):
        authority = []
        for i in range(1, 9):
            authority.append(str(
                getattr(self, 'authority'+str(i)).checkState())
            )
        return ''.join(authority)

    def save_data(self, item):
        try:
            data = item.text()
        except AttributeError:
            data = item.currentText()
        if data:
            self.dept_data[item.objectName()] = data
        else:
            try:
                self.dept_data.pop(item.objectName())
            except ValueError:
                pass
