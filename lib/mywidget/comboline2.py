from PyQt5 import QtWidgets, QtCore, QtGui
from lib.mywidget.mylineedit import myLineEdit
from lib.utils.saveexcept import SaveExcept
from django.db.models import Q


class ComboLine(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # 下拉列表的内容字段
        self.valuetuple = tuple()
        # 查询的关键字
        self.key = set()
        _translate = QtCore.QCoreApplication.translate
        # 需要加载的数据库对象
        self.module_name = None
        self.name = myLineEdit(parent)
        self.name.setObjectName("name")
        self.namelist = QtWidgets.QTreeWidget(parent)
        self.namelist.setObjectName("namelist")
        self.namelist.setVisible(False)
        font = QtGui.QFont()
        font.setFamily("宋体")
        font.setPointSize(11)
        self.namelist.setFont(font)
        self.namelist.setStyleSheet("background-color: rgb(255, 255, 125);")
        self.namelist.setTabKeyNavigation(False)
        self.namelist.setIndentation(20)
        self.namelist.setRootIsDecorated(False)
        self.namelist.setUniformRowHeights(False)
        self.namelist.setItemsExpandable(True)
        self.namelist.setAnimated(False)
        self.namelist.setAllColumnsShowFocus(False)
        self.namelist.setFocusPolicy(QtCore.Qt.NoFocus)
        self.namelist.setWordWrap(False)
        self.namelist.setHeaderHidden(False)
        self.namelist.setExpandsOnDoubleClick(True)
        self.namelist.setObjectName("namelist")
        #self.namelist.header().setVisible(True)
        # self.textChanged.connect(self.setname2)
        self.name.textChanged.connect(self.on_name_textEdited)
        self.name.sendmsg.connect(self.inputreject)
        self.name.acceptmsg.connect(self.setname)
        self.namelist.itemDoubleClicked.connect(self.setname)
        self.name.returnPressed.connect(self.setname)

    def moveEvent(self, *args, **kwargs):
        self.namelist.move(self.geometry().x(), self.geometry().y() + 20)

    def setGeometry(self, *__args):
        rect = QtCore.QRect(*__args)
        self.namelist.move(rect.x(), rect.y() + 20)

    def setup(self, row: tuple, key: set, db_table, row_name=None):
        try:
            self.valuetuple = row
            for item in key:
                self.key.add(item + '__icontains')
            db_module = __import__('db.models', fromlist=('models',))
            self.module_name = getattr(db_module, db_table)
            if row_name is not None:
                # 把列表的宽度设置为除id行外每列按120算
                self.namelist.setFixedWidth((len(row_name) - 1) * 150)
                self.namelist.setFixedHeight(200)
                try:
                    for key in range(len(row_name)):
                        self.namelist.headerItem().setText(key, row_name[key])
                except TypeError:
                    self.namelist.header().setVisible(False)
        except:
            pass

    # 获得当前项目的id
    def get_item(self):
        try:
            item = self.namelist.currentItem()
            return item.text(0), item.text(1), item.text(2), item.text(3), item.text(4), item.text(5)
        except AttributeError:
            return None

    def focusOutEvent(self, e):
        print(1)
        self.setname()
        self.name.focusOutEvent(self.name, e)

    def raise_(self):
        self.name.raise_()
        self.namelist.raise_()

    def inputreject(self, e):
        self.namelist.keyPressEvent(e)
        print(self.namelist.selectedItems())

    def setname(self):
        try:
            name_id = self.namelist.currentItem().text(1)
            name = self.namelist.currentItem().text(2)
            self.name.setText(name_id + ' ' + name)
            self.namelist.setVisible(False)
        #except AttributeError:
        #    pass
        except Exception as e:
            print(e)

    def on_name_textEdited(self, p_str):
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
                for i in range(1, 8):
                    self.namelist.resizeColumnToContents(i)
                    if self.namelist.columnWidth(i) > 150:
                        self.namelist.setColumnWidth(i, 150)
                # self.it = QtWidgets.QTreeWidgetItemIterator(self.namelist)
            else:
                self.namelist.clear()
                self.namelist.setVisible(False)
                self.namelist.setStyleSheet(
                    "background-color: rgb(255, 255, 255)")
        else:
            self.namelist.clear()
            self.namelist.setVisible(False)
            self.namelist.setStyleSheet(
                "background-color: rgb(255, 255, 255)")
