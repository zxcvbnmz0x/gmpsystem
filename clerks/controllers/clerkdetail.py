from PyQt5 import QtCore, QtGui, QtWidgets
import json
import datetime

from clerks.views.clerkdetailUI import Ui_Dialog

from clerks.models.deptclerkmodel import DeptClerkModel

from lib.utils.inputcode import Inputcode
from lib.utils.authority import Authority

class ClerkDtail(QtCore.QObject, Ui_Dialog):
    # 自定义信号，用于传递部门编号，部门名称，上级部门Id，部门权限
    # getData = QtCore.pyqtSignal(dict)

    def __init__(self, clerk_id=""):
        # 根据人员权限确定是否能打开模块；是否能修改人员信息
        super().__init__()
        self.isVisible = 0
        if clerk_id:
            clerk_authority = Authority().get_authoriy(clerk_id)
            if clerk_authority:
                self.authority = json.loads(clerk_authority[0])["1"]["1"]
                if self.authority == 2:
                    self.isVisible = 1
                elif self.authority == 0:
                    raise Exception
                else:
                    self.isVisible = 0

        # 用于传递修改的数据记录
        self.data = {}
        # 当前人员信息
        self.clerkdetail = {}
        # 填写错误的信息
        self.error_msg = {}
        # 初始化对话框
        self.dialog = QtWidgets.QDialog()
        # 数据库操作
        self.dept_clerk_model = DeptClerkModel()
        self.setupUi(self.dialog)

        # 当前人员的clerkid,主键
        self.clerk_id = clerk_id
        # 初始化填写格式
        self.init_lineedit_content()
        # 初始化权限列表
        self.init_authority()
        # 初始化下拉菜单的内容
        self.init_combo_content(
            edudegree=self.edudegree, techtitle=self.techtitle
        )

    # 显示对话框
    # tittle    对话框的标题名
    # accept    确认按键的显示内容
    # cancel    取消按键的显示内容
    def show(self, title="编辑人员资料", accept="确定", cancel="取消"):
        # 设置对话框标题、确认和取消按键的显示内容
        self.dialog.setWindowTitle(title)
        if self.isVisible == 0:
            self.accept.setEnabled(False)
            self.cancel.setEnabled(False)
        else:
            self.accept.setText(accept)
            self.cancel.setText(cancel)
        if self.clerk_id:
            res = self.dept_clerk_model.get_clerk(self.clerk_id)
            if res:
                # 把获取到的人员信息填写到表格中
                self.set_clerk_detail(res[0])
        # 初始化信号和槽的连接
        self.signal_connect_slot()
        # 显示对话框
        self.dialog.exec_()

    # 输入码动态关联部门名称
    # 使用pypinyin，style设置为Style.FIRST_LETTER
    # 用join拼接生成的结果
    # 把结果转成大写后传递给self.inputCode
    '''
    def inputcode_change(self, qstr):
        input_name = pinyin(qstr, style=Style.FIRST_LETTER)
        output = []
        for key in range(len(input_name)):
            output.append(input_name[key][0])
        outputcode = ''.join(output)
        self.inputCode.setText(outputcode.upper())
    '''

    def set_item(self, itemname, itemvalue):
        getattr(self, itemname).setText(itemvalue)

    def set_clerk_detail(self, detail):
        self.clerkdetail = detail
        self.clerkid.setText(detail['pid'])
        self.clerkname.setText(detail['clerkname'])
        self.inputcode.setText(detail['inputcode'])
        self.sex.setCurrentText(detail['sex'])
        self.birthday.setText(str(detail['birthday']))
        self.marrystatus.setCurrentText(detail['marrystatus'])
        self.nation.setCurrentText(detail['nation'])
        self.native_2.setText(detail['native'])
        self.policystatus.setCurrentText(detail['policystatus'])
        self.idno.setText(detail['idno'])
        self.address.setText(detail['address'])
        self.telno.setText(detail['telno'])
        self.entranceday.setText(str(detail['entranceday']))
        self.edudegree.setCurrentText(detail['edudegree'])
        self.special.setText(detail['special'])
        self.schoolname.setText(detail['schoolname'])
        self.techtitle.setCurrentText(detail['techtitle'])
        self.strongsuit.setText(detail['strongsuit'])
        # 设置人员权限
        self.set_powers(json.loads(detail['powers']))

    # 设置人员权限
    # powers：当前的权限，json
    # 格式如下：
    # {"1": {"1": 2,"2": {"1": 2,"2": 2,"3": 0}},
    #  "2":{"1":2},"3": {"1": 0,"2": 2}
    # }
    # 键值为列表中的第几项，该项的状态又子项目决定，如果没有子项目则由值决定
    def set_powers(self, powers):
        for key, item in powers.items():
            # 获取小数点前的序号，'cbchbox_' + str(key)即为复选框的objname
            # 获得当前权限部件对象
            cbchbox = getattr(self, 'cbchbox_' + str(key))
            try:
                power_list = item
                self.set_current_power(cbchbox, power_list)
            except IndexError:
                # 直接把这个项目设置为2
                cbchbox.setCurrentIndex(2)

    # 设置当前权限下的子权限
    # 使用递归设置
    # widget：控件对象
    # power_list：权限
    def set_current_power(self, widget, power_list):
        # check_state用于设置按键的状态，如check_state[1]就是半选择的状态
        check_state = [QtCore.Qt.Unchecked, QtCore.Qt.PartiallyChecked,
                       QtCore.Qt.Checked]
        for key, value in power_list.items():
            # 获得当前层级序号为int(key)-1的部件
            tree_item = widget.qListWidget.topLevelItem(int(key) - 1)
            # 获得树项目里的部件，即下一级的部件
            combobox = widget.qListWidget.itemWidget(tree_item, 0)
            if type(value).__name__ == 'dict':
                # 把下一级部件的内容继续循环生成
                self.set_current_power(combobox, value)
            elif value in (0, 2):
                combobox.setCheckState(check_state[int(value)])

    # 把所有预定义好的信号连接到槽
    def signal_connect_slot(self):
        self.setimage.clicked.connect(self.on_setimage_clicked)
        self.accept.clicked.connect(self.on_accept_clicked)
        self.cancel.clicked.connect(self.on_cancel_clicked)
        self.clerkid.textChanged.connect(self.on_clerkid_textChanged)
        self.clerkname.textChanged.connect(self.on_clerkname_textChanged)
        self.inputcode.textChanged.connect(self.on_inputcode_textChanged)
        self.sex.currentTextChanged.connect(self.on_sex_currentTextChanged)
        self.birthday.textChanged.connect(self.on_birthday_textChanged)
        self.marrystatus.currentTextChanged.connect(self.on_marrystatus_currentTextChanged)
        self.nation.currentTextChanged.connect(self.on_nation_currentTextChanged)
        self.native_2.textChanged.connect(self.on_native_2_textChanged)
        self.policystatus.currentTextChanged.connect(self.on_policystatus_currentTextChanged)
        self.idno.textChanged.connect(self.on_idno_textChanged)
        self.address.textChanged.connect(self.on_address_textChanged)
        self.telno.textChanged.connect(self.on_address_textChanged)
        self.entranceday.textChanged.connect(self.on_entranceday_textChanged)
        self.edudegree.currentTextChanged.connect(self.on_edudegree_currentTextChanged)
        self.special.textChanged.connect(self.on_special_textChanged)
        self.schoolname.textChanged.connect(self.on_schoolname_textChanged)
        self.techtitle.currentTextChanged.connect(self.on_techtitle_currentTextChanged)
        self.strongsuit.textChanged.connect(self.on_strongsuit_textChanged)

    # 校验人员编号的修改
    def on_clerkid_textChanged(self, text):
        if text != self.clerkdetail['clerkid']:
            self.data['clerkid'] = text
        else:
            try:
                del self.data['clerkid']
            except KeyError:
                pass

    # 人员姓名
    def on_clerkname_textChanged(self, text):
        if text != self.clerkdetail['clerkname']:
            self.data['clerkname'] = text
            # 把人员名称拼音关联到输入码
            self.inputcode.setText(Inputcode.make_inputcode(text))
        else:
            try:
                del self.data['clerkname']
            except KeyError:
                pass

    # 快速输入码
    def on_inputcode_textChanged(self, text):
        if text != self.clerkdetail['inputcode']:
            self.data['inputcode'] = text
        else:
            try:
                del self.data['inputcode']
            except KeyError:
                pass


    # 性别
    def on_sex_currentTextChanged(self, text):
        if text != self.clerkdetail['sex']:
            self.data['sex'] = text
        else:
            try:
                del self.data['sex']
            except KeyError:
                pass

    # 出生日期
    def on_birthday_textChanged(self, text):
        if text != self.clerkdetail['birthday']:
            try:
                self.data['birthday'] = datetime.datetime.strptime(text,
                                                                      "%Y-%m-%d")
            except ValueError:
                self.error_msg['birthday'] = "雇佣日期格式不正确，格式应为2019-04-20；"
        else:
            try:
                del self.data['birthday']
            except KeyError:
                pass

    # 婚姻状态
    def on_marrystatus_currentTextChanged(self, text):
        if text != self.clerkdetail['marrystatus']:
            self.data['marrystatus'] = text
        else:
            try:
                del self.data['marrystatus']
            except KeyError:
                pass

    # 民族
    def on_nation_currentTextChanged(self, text):
        if text != self.clerkdetail['nation']:
            self.data['nation'] = text
        else:
            try:
                del self.data['nation']
            except KeyError:
                pass

    # 籍贯
    def on_native_2_textChanged(self, text):
        if text != self.clerkdetail['native']:
            self.data['native'] = text
        else:
            try:
                del self.data['native']
            except KeyError:
                pass

    # 政治面貌
    def on_policystatus_currentTextChanged(self, text):
        if text != self.clerkdetail['policystatus']:
            self.data['policystatus'] = text
        else:
            try:
                del self.data['policystatus']
            except KeyError:
                pass

    # 身份证号码
    def on_idno_textChanged(self, text):
        if text != self.clerkdetail['idno']:
            if len(text) == 18:
                self.data['idno'] = text
            else:
                self.error_msg['idno'] = "身份证号应为18位数字；"
        else:
            try:
                del self.data['idno']
            except KeyError:
                pass

    #
    def on_address_textChanged(self, text):
        if text != self.clerkdetail['address']:
            self.data['address'] = text
        else:
            try:
                del self.data['address']
            except KeyError:
                pass

    # 雇佣日期
    def on_entranceday_textChanged(self, text):
        if text != self.clerkdetail['entranceday']:
            try:
                self.data['entranceday'] = datetime.datetime.strptime(text, "%Y-%m-%d")
            except ValueError:
                self.error_msg['entranceday'] = "雇佣日期格式不正确，格式应为2019-04-20；"
        else:
            try:
                del self.data['entranceday']
            except KeyError:
                pass

    # 文化程度
    def on_edudegree_currentTextChanged(self, text):
        if text != self.clerkdetail['edudegree']:
            self.data['edudegree'] = text
        else:
            try:
                del self.data['edudegree']
            except KeyError:
                pass

    # 专业
    def on_special_textChanged(self, text):
        if text != self.clerkdetail['special']:
            self.data['special'] = text
        else:
            try:
                del self.data['special']
            except KeyError:
                pass

    # 毕业学校
    def on_schoolname_textChanged(self, text):
        if text != self.clerkdetail['schoolname']:
            self.data['schoolname'] = text
        else:
            try:
                del self.data['schoolname']
            except KeyError:
                pass

    # 职称
    def on_techtitle_currentTextChanged(self, text):
        if text != self.clerkdetail['techtitle']:
            self.data['techtitle'] = text
        else:
            try:
                del self.data['techtitle']
            except KeyError:
                pass

    # 工作前年限
    def on_strongsuit_textChanged(self, text):
        if text != self.clerkdetail['strongsuit']:
            try:
                strongsuit = int(text)
                self.data['strongsuit'] = strongsuit
            except ValueError:
                self.error_msg['strongsuit'] = "工作前年限格式错误，请输入数字；"
            else:
                try:
                    del self.data['strongsuit']
                except KeyError:
                    pass

    # 上传图片功能
    def on_setimage_clicked(self):
        img_name, img_type = QtWidgets.QFileDialog.getOpenFileName(
            self.clerk_image, "打开图片", "c:\\", "*.jpg;;*.png;;All Files(*)")
        jpg = QtGui.QPixmap(img_name).scaled(
            self.clerk_image.width(), self.clerk_image.height()
        )
        self.clerk_image.setPixmap(jpg)

    # 取消功能
    def on_cancel_clicked(self):
        self.dialog.close()

    # 确认功能
    def on_accept_clicked(self):
        if not self.error_msg:
            if self.data:
                # self.getData.emit(self.data)
                res = self.dept_clerk_model.update_clerk_detail(self.data,
                                                                self.clerk_id)
                if res:
                    self.dialog.accept()
                else:
                    warmdialog = QtWidgets.QMessageBox()
                    warmdialog.setWindowTitle("更新数据出错")
                    warmdialog.setIcon(QtWidgets.QMessageBox.Warning)
                    warmdialog.setText(res)
                    # 添加Yes和No2个按键
                    warmdialog.setStandardButtons(
                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                    # 设置按键的文本为“确认”和“取消”
                    button_yes = warmdialog.button(QtWidgets.QMessageBox.Yes)
                    button_yes.setText("确认")
                    button_no = warmdialog.button(QtWidgets.QMessageBox.No)
                    button_no.setText("取消")

                    message = warmdialog.exec_()
                    if message == QtWidgets.QMessageBox.Yes:
                        # 把当前选择的部门添加到上级部门中
                        self.on_accept_clicked()
                        return
            else:
                self.dialog.accept()
        else:
            warmdialog = QtWidgets.QMessageBox()
            warmdialog.setWindowTitle("请选择合适的部门")
            warmdialog.setIcon(QtWidgets.QMessageBox.Warning)
            warmdialog.setText("记录保存失败，填写的记录存在以下错误：")
            # 添加Yes和No2个按键
            warmdialog.setStandardButtons(
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            # 设置按键的文本为“确认”和“取消”
            button_yes = warmdialog.button(QtWidgets.QMessageBox.Yes)
            button_yes.setText("确认")
            button_no = warmdialog.button(QtWidgets.QMessageBox.Yes)
            button_no.setText("取消")
            p_str = ""
            for item in self.error_msg:
                p_str = p_str +"●" + self.error_msg[item] + '\n'
            warmdialog.setInformativeText(p_str)
            message = warmdialog.exec_()
            if message == QtWidgets.QMessageBox.Yes:
                return

    # 初始化填写内容的格式
    def init_lineedit_content(self):
        # 入职前工作年限，格式应该为纯数字
        double_valitor = QtGui.QDoubleValidator()
        double_valitor.setRange(0, 100)
        double_valitor.setNotation(QtGui.QDoubleValidator.StandardNotation)
        double_valitor.setDecimals(1)
        self.strongsuit.setValidator(double_valitor)

        # 出生日期、雇佣日期，格式yyyy-MM-DD
        reg = QtCore.QRegExp('^[23][0-9]{3}-[0-9]{2}-[0-9]{2}$')
        day_validator = QtGui.QRegExpValidator()
        day_validator.setRegExp(reg)
        self.birthday.setValidator(day_validator)
        self.entranceday.setValidator(day_validator)

        # 匹配身份证
        reg = QtCore.QRegExp('^\d{17}(\d|X)$')
        id_validator = QtGui.QRegExpValidator()
        id_validator.setRegExp(reg)
        self.idno.setValidator(id_validator)

        # 匹配电话号码，纯数字
        reg = QtCore.QRegExp('[0-9]{11}')
        tel_validator = QtGui.QRegExpValidator()
        tel_validator.setRegExp(reg)
        self.telno.setValidator(tel_validator)

    # 初始化下拉列表
    def init_combo_content(self, **kwargs):
        for key, value in kwargs.items():
            res = self.dept_clerk_model.get_content(key)
            if res:
                value.addItems(res)
                value.setCurrentText("")

    # 初始化权限列表
    def init_authority(self):
        self.cbchbox_1.setcbchbox_name(self.cbchbox_1, CBCBOX_1_TEXT)
        self.cbchbox_1.setlist(self.cbchbox_1, "", CBCHBOX_1_ITEMS)
        self.cbchbox_2.setcbchbox_name(self.cbchbox_2, CBCBOX_2_TEXT)
        self.cbchbox_2.setlist(self.cbchbox_2, "", CBCHBOX_2_ITEMS)
        self.cbchbox_3.setcbchbox_name(self.cbchbox_3, CBCBOX_3_TEXT)
        self.cbchbox_3.setlist(self.cbchbox_3, "", CBCHBOX_3_ITEMS)
        self.cbchbox_4.setcbchbox_name(self.cbchbox_4, CBCBOX_4_TEXT)
        self.cbchbox_4.setlist(self.cbchbox_4, "", CBCHBOX_4_ITEMS)
        self.cbchbox_5.setcbchbox_name(self.cbchbox_5, CBCBOX_5_TEXT)
        self.cbchbox_5.setlist(self.cbchbox_5, "", CBCHBOX_5_ITEMS)
        self.cbchbox_6.setcbchbox_name(self.cbchbox_6, CBCBOX_6_TEXT)
        self.cbchbox_6.setlist(self.cbchbox_6, "", CBCHBOX_6_ITEMS)
        self.cbchbox_7.setcbchbox_name(self.cbchbox_7, CBCBOX_7_TEXT)
        self.cbchbox_7.setlist(self.cbchbox_7, "", CBCHBOX_7_ITEMS)
        self.cbchbox_8.setcbchbox_name(self.cbchbox_8, CBCBOX_8_TEXT)
        self.cbchbox_8.setlist(self.cbchbox_8, "", CBCHBOX_8_ITEMS)
        self.cbchbox_9.setcbchbox_name(self.cbchbox_9, CBCBOX_9_TEXT)
        self.cbchbox_9.setlist(self.cbchbox_9, "", CBCHBOX_9_ITEMS)


CBCBOX_1_TEXT = "基础资料"
CBCBOX_2_TEXT = "采购管理"
CBCBOX_3_TEXT = "质量管理"
CBCBOX_4_TEXT = "生产管理"
CBCBOX_5_TEXT = "仓库管理"
CBCBOX_6_TEXT = "设备管理"
CBCBOX_7_TEXT = "销售管理"
CBCBOX_8_TEXT = "综合管理"
CBCBOX_9_TEXT = "物资管理"

CBCHBOX_1_ITEMS = [{"部门员工管理": ["查看", "编辑", "权限"]},
                   {"物料字典": ["查看", "编辑", "权限", "打印"]}, "产品字典", "供应商管理",
                   "自定义文档", "生产线定义", "系统设置"]
CBCHBOX_2_ITEMS = ["采购计划", ]
CBCHBOX_3_ITEMS = ["请验取样", "检验报告", "生产审核放行", "留样记录",
                   "验证文档", "质量辅助记录", "环境监测报告",
                   "偏差/不合格处理", "物料检验项目设置", "日常检验项目设置",
                   "原始检验记录设置", "自检记录", "自检项目设置"]
CBCHBOX_4_ITEMS = ["生产指令", "生产车间", "半成品登记", "半成品发放",
                   "物料寄存登记", "物料发放", "生产审核放行", "生产辅助记录",
                   "岗位工人", "温湿度记录"]
CBCHBOX_5_ITEMS = ["进货登记", "物料采购入库", "物料入库单", "物料出库单",
                   "产品寄库", "零头寄库", "产品出库", "半成品/前处理入库",
                   "生产领料", "产品零头领取", "产品入库", "生产退料",
                   "物料调拨", "物料库存", "产品库存", "退货处理", "退货登记"]
CBCHBOX_6_ITEMS = ["设备资料", "设备运行记录", "润滑记录", "维护记录",
                   "事故记录", "一般记录", "纯化水申验", "注射用水申验", "维护事件"]
CBCHBOX_7_ITEMS = ["销售订单", "回款记录", "退款记录", "客户管理"]
CBCHBOX_8_ITEMS = ["客户投诉", "培训健康记录", "文档管理", "二维码入库文件",
                   "二维码出库文件", "二维码退库文件", "二维码库"]
CBCHBOX_9_ITEMS = ["物资请购", "物资入库", "物资领取"]
