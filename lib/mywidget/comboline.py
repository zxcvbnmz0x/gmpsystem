from PyQt5 import QtWidgets, QtCore, QtGui
from lib.mywidget.mylineedit import myLineEdit
from lib.utils.saveexcept import SaveExcept
from django.db.models import Q


class ComboLine(myLineEdit):
    getItem = QtCore.pyqtSignal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        # 下拉列表的内容字段
        self.valuetuple = tuple()
        # 查询的关键字
        self.key = set()
        self.flat = 1
        _translate = QtCore.QCoreApplication.translate
        # 需要加载的数据库对象
        self.module_name = None
        self.row_name = None
        self.namelist = QtWidgets.QTreeWidget(parent)
        self.namelist.setObjectName("namelist")
        self.namelist.setVisible(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.namelist.setFont(font)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.namelist.setStyleSheet("background-color: rgb(255, 255, 125);")
        self.namelist.setTabKeyNavigation(False)
        self.namelist.setIndentation(20)
        self.namelist.setRootIsDecorated(False)
        self.namelist.setUniformRowHeights(False)
        self.namelist.setItemsExpandable(True)
        self.namelist.setAnimated(False)
        self.namelist.setAllColumnsShowFocus(False)
        self.namelist.setWordWrap(False)
        self.namelist.setHeaderHidden(False)
        self.namelist.setExpandsOnDoubleClick(True)
        self.namelist.setObjectName("namelist")
        self.namelist.header().setVisible(True)
        self.namelist.setFocusPolicy(QtCore.Qt.NoFocus)
        self.textEdited.connect(self.on_name_textEdited)
        self.sendmsg.connect(self.inputreject)
        self.acceptmsg.connect(self.setname)
        self.namelist.itemDoubleClicked.connect(self.setname)
        self.returnPressed.connect(self.setname)

    def moveEvent(self, *args, **kwargs):
        self.namelist.move(self.geometry().x(), self.geometry().y() + 20)

    def setGeometry(self, *__args):
        rect = QtCore.QRect(*__args)
        self.move(rect.x(), rect.y())
        self.resize(rect.width(), rect.height())
        self.namelist.move(rect.x(), rect.y() + 20)

    def setup(self, db_table: str, row: tuple, key: set, row_name: list,
              treewidth: int = 200, treeheight: int = 200):
        """ 初始化下拉输入框
        生产的语句格式：select row from db_table where key like '%str'
        参数
        ---------------------
        db_table :str
            数据表名
        row : tuple
            查询返回数据表列名
        key : set
            要进行比较的数据表列名
        row_name : list
            下拉列表中的表头名
        treewidth: int
            下拉列表的宽度
        treeheight: int
            下拉列表的高度
        """
        self.namelist.resize(treewidth, treeheight)
        self.row_name = row_name
        try:
            self.valuetuple = row
            self.key.clear()
            for item in key:
                self.key.add(item + '__icontains')
            db_module = __import__('db.models', fromlist=['models'])
            self.module_name = getattr(db_module, db_table)
            if row_name:
                # 把列表的宽度设置为除id行外每列按120算
                # self.namelist.setFixedWidth((len(row_name) - 1) * 150)
                # self.namelist.setFixedHeight(200)
                try:
                    for key in range(len(row_name)):
                        self.namelist.headerItem().setText(key, row_name[key])
                except TypeError:
                    self.namelist.header().setVisible(False)
            else:
                self.namelist.header().setVisible(False)
        except Exception as e:
            SaveExcept(e, "下来菜单设置数据表出错", db_table=db_table, row=row, key=key,
                       row_name=row_name)

    # 获得当前项目的id
    def get_item(self):
        try:
            return self.namelist.currentItem()
        except AttributeError:
            return ''

    def setText(self, p_str):
        if len(p_str):
            self.setStyleSheet("background-color: rgb(255, 255, 125);")
        else:
            self.setStyleSheet("background-color: rgb(255, 255, 255);")
        super(ComboLine, self).setText(p_str)

    def raise_(self):
        self.namelist.raise_()

    def inputreject(self, e):
        self.namelist.keyPressEvent(e)

    def setname(self):
        try:
            name_id = self.namelist.currentItem().text(1)
            name = self.namelist.currentItem().text(2)
            self.setText(name_id + ' ' + name)
            self.getItem.emit(self.get_item())
            self.namelist.setVisible(False)
            self.setStyleSheet("background-color: rgb(255, 255, 125);")
            self.flat = 1
        except:
            self.setStyleSheet("background-color: rgb(255, 255, 255);")

    def on_name_textEdited(self, p_str):
        if self.flat:
            self.flat = 0
        if p_str:
            filter_content = Q()
            for item in self.key:
                try:
                    kwargs = {item: p_str}
                    if filter_content != Q:
                        filter_content = filter_content | Q(**kwargs)
                    else:
                        filter_content = Q(**kwargs)
                except Exception as e:
                    SaveExcept(e, "查询字典内容出错", self.key, self.module_name,
                               self.valuetuple)
            res = self.module_name.objects.filter(filter_content).values_list(
                *self.valuetuple)
            if res:
                self.namelist.clear()
                self.namelist.setVisible(True)
                self.namelist.setStyleSheet(
                    "background-color: rgb(255, 255, 125)")
                for k, item in enumerate(res):
                    user = QtWidgets.QTreeWidgetItem(self.namelist)
                    for key in range(len(item)):
                        user.setText(key, str(item[key]))
                    if k == 0:
                        self.namelist.setCurrentItem(user, 1)

                # 隐藏第一列的id
                self.namelist.hideColumn(0)
                for i in range(1, len(self.row_name)):
                    self.namelist.resizeColumnToContents(i)
                    if self.namelist.columnWidth(i) > 150:
                        self.namelist.setColumnWidth(i, 120)

            else:
                self.namelist.clear()
                self.namelist.setVisible(0)
                self.namelist.setVisible(False)
                self.namelist.setStyleSheet(
                    "background-color: rgb(255, 255, 255)")
        else:
            self.namelist.clear()
            self.namelist.setVisible(0)
            self.namelist.setVisible(False)
            self.namelist.setStyleSheet(
                "background-color: rgb(255, 255, 255)")
