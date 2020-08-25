import sys
import decimal
import re

from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import Qt

import user as userdetail
from lib.utils.evalenv import evalenv
from db.models import Selfdefinedformat, Forms
from product.controllers.productcontroller import ProductController
from stuff.controllers.stuffcontroller import StuffController
from labrecord.controllers.labrecordscontroller import LabrecordsController

from lib.xmlwidget.xmlcheckbox import XmlCheckBox
from lib.xmlwidget.xmlcombobox import XmlComboBox
from lib.xmlwidget.xmlexprbox import XmlExprBox
from lib.xmlwidget.xmllineedit import XmlLineEdit
from lib.xmlwidget.xmlsignbox import XmlSignBox
from lib.xmlwidget.xmltextedit import XmlTextEdit

from tesui import Ui_Form

# 批记录产品信息类变量
PRODUCT_DICT = {'PBIANHAO': 'prodid', 'PMING': 'prodname', 'PGUIGE': 'spec',
                'PBZGG': 'package', 'PTMING': 'commonname', 'PPIHAO': 'batchno',
                'PSHIJI': 'realamount', 'PJIHUA': 'planamount',
                'PJIXING': 'medkind'
                }
# 批记录物料信息类变量
STUFF_DICT = {'ID': 'stuffid', 'MING': 'stuffname', 'PIHAO': 'batchno',
              'LEIBIE': 'kind', 'GUIGE': 'spec', 'BZGG': 'package',
              'JBDW': 'unit', 'XBZDW': 'spunit', 'ZBZDW': 'mpunit',
              'DBZDW': 'bpunit',
              'JIHUA': 'presamount', 'SHIJI': 'realamount',
              'LINGQU': 'drawamount',
              'SHENGYU': 'restamount', 'TUIKU': 'backamount',
              'SHUIFEN': 'water',
              'HANLIANG': 'content', 'CHANGJIA': 'producer'
              }
STUFF_KIND = {'ZF': (0, 1), 'ZC': 0, 'FC': 1, 'NB': 2, 'WB': 3, 'BC': (2, 3),
              'QC': 4}
# 检验报告类信息变量
# 检品编号，检品名称，批号，半成品取样，成品取样，生产厂家，报告编号，检品数量
LAB_DICT = {'SID': 'chkid', 'SMING': 'chkname', 'JPPIHAO': 'batchno',
            'MQUYANG': 'samplecount', 'PQUYANG': 'samplecount',
            'SPRODUCER': 'producer', 'SBGBH': 'paperno',
            'JPSHULIANG': 'checkamount'
            }

# 对齐方式
alignment = ('L', 'C', 'R')
qtalign = (Qt.AlignLeft, Qt.AlignHCenter, Qt.AlignRight)


class ReadXML(QDialog, Ui_Form):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.reader = QtCore.QXmlStreamReader()
        self.writer = QtXmlPatterns.QXmlQuery()
        # self.pix = QtGui.QPixmap(800, 600)
        # self.pix.fill(QtCore.Qt.white)
        # 线框，先把所有线框的信息都保存了，最后再刷新
        self.line_border = list()

        self.current_X = 20
        self.current_Y = 10
        self.form = parent
        # 要查询的记录id
        self.autoid = 0
        # 要查询的内容,0测试，1生产，2检验
        self.type = 0
        self.proddetail = None
        self.stuffdetail = None
        self.mstuffdetail = None
        self.labdetail = None
        self.stuffdetailZF = list()
        self.stuffdetailZC = list()
        self.stuffdetailFC = list()
        self.stuffdetailNB = list()
        self.stuffdetailWB = list()
        self.stuffdetailBC = list()
        self.stuffdetailQC = list()

        self.stuffdetailMZF = list()
        self.stuffdetailMZC = list()
        self.stuffdetailMFC = list()
        self.stuffdetailMNB = list()
        self.stuffdetailMWB = list()
        self.stuffdetailMBC = list()
        self.stuffdetailMQC = list()

    # 中文：14个像素 英文：7个像素，系统中的长度*7 = 像素
    # 中文数*2 = 系统中的长度，中位数*14 = 像素
    # 系统中长度*7 = 像素
    def read(self, file):

        # 传入的是地址
        qfile = QtCore.QFile(file)
        # 找到文件,则设置引擎,否则向xml文件直接添加数据
        if qfile.open(QtCore.QFile.ReadWrite | QtCore.QFile.Text):
            self.reader.setDevice(file)
            self.writer.setDevice(file)
        else:
            self.reader.addData(file)
            s = self.writer.setQuery(file + '/GMPPaper/Title[2]')
            print(s)
        self.reader.setNamespaceProcessing(0)
        self.reader.readNextStartElement()
        if self.reader.isStartDocument():
            self.reader.readNextStartElement()
        # 如果没有读到文档结尾，而且没有出现错误
        while not self.reader.atEnd():
            if self.reader.isStartElement():
                name = self.reader.name()
                if name == "GMPPaper":
                    pass
                # 标题框
                elif name == "Title":
                    self.titleBox()
                # 标题输入框
                elif name == "TextBox":
                    self.inputBox()
                # 线框
                elif name == "Box":
                    self.wireframe()
                # 检测框
                elif name == "CheckBox":
                    self.checkBox()
                # 下拉框
                elif name == "ComboBox":
                    self.comboBox()
                # 签名框
                elif name == "Signature":
                    self.signBox()
                elif name == "Expr":
                    self.exprBox()
                elif name == "br":
                    self.wrapBox()
            # 空格组成的字符，包括换行
            elif self.reader.isWhitespace():
                pass
            # 纯文本
            elif self.reader.isCharacters():
                pass
            self.reader.readNextStartElement()
            # 如果读取过程中出现错误，那么输出错误信息
            # if self.reader.hasError():
            #    print(self.reader.errorString())
            # raise ValueError
        if qfile.isOpen():
            qfile.close()
        # self.update()
        self.scrollAreaWidgetContents.setLineBorder(self.line_border)
        '''
        try:

        except Exception as e:
            print(repr(e))
            pass
            # raise ValueError
        '''

    # 标题框
    def titleBox(self):
        widget = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        widget.setContentsMargins(2, 0, 0, 0)
        self.boxresize(widget)
        # L C R ,左中右对齐
        align = self.reader.attributes().value("align")
        widget.setAlignment(
            QtCore.Qt.AlignVCenter | qtalign[alignment.index(align)])
        widget.setText(self.set_vars(self.reader.readElementText()))

    # 输入框
    def inputBox(self):
        widgetlabel = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        widgetlineedit = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        # self.reader.lineNumber()

        # widgetlineedit.setObjectName('widget' + self.reader.columnNumber())
        widgetlabel.setContentsMargins(2, 0, 0, 0)
        widgetlineedit.setContentsMargins(1, 0, 1, 0)
        # self.boxresize(widgetlineedit)
        widgetlabel.move(self.current_X, self.current_Y)
        widgetlabel.setText(
            self.set_vars(self.reader.attributes().value("Title")))
        widgetlineedit.editingFinished.connect(self.widgetedit)

        L_width = int(self.reader.attributes().value("Width")) * 7
        L_height = int(self.reader.attributes().value(
            "Height")) * 7 if self.reader.attributes().value(
            "Height") else 20
        if L_width:
            # 标题长度不为0
            widgetlabel.resize(L_width, L_height)
            self.current_X += L_width
        else:
            # 标题内容不为空
            if self.reader.attributes().value("Title"):
                widgetlabel.adjustSize()
                widgetlabel.resize(widgetlabel.size().width(), L_height)
            else:
                widgetlabel.resize(0, L_height)
            self.current_X += widgetlabel.size().width()
        self.boxresize(widgetlineedit, "MaxLength", "MaxHeight")
        wid = self.reader.attributes().value("ID")
        widgetlineedit.setText(self.set_vars(self.reader.readElementText()))
        if wid:
            try:
                setattr(self, wid, decimal.Decimal(widgetlineedit.text()))
            except:
                setattr(self, wid, '')

    # 线框
    def wireframe(self):
        linewidth = int(self.reader.attributes().value("width")) * 7
        lineheight = int(self.reader.attributes().value("height")) * 20
        penwidth = int(self.reader.attributes().value("PenWidth"))

        qrect = QtCore.QRect(self.current_X, self.current_Y, linewidth,
                             lineheight)

        self.line_border.append((qrect, penwidth))

    # 检测框
    def checkBox(self):
        self.reader.readNextStartElement()
        widget = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
        # widget.setContentsMargins(2, 0, 0, 0)
        self.boxresize(widget)
        widget.setText(self.set_vars(self.reader.attributes().value("name")))
        widget.setChecked(int(self.reader.readElementText()))
        # self.boxresize(widget)

    # 下拉框
    def comboBox(self):
        index = 0
        widget = QtWidgets.QComboBox(self.scrollAreaWidgetContents)
        self.boxresize(widget)

        # 允许自己填内容，则显示“value”的内容，
        # 否则显示index序号的内容
        if int(self.reader.attributes().value("style")):
            widget.setEditable(
                int(self.reader.attributes().value("style")))
            widget.setCurrentText(
                self.reader.attributes().value("value"))
        else:
            index = int(self.reader.attributes().value("index"))
        # self.boxresize(widget)
        # 循环添加下拉菜单的项目。
        while 1:
            self.reader.readNext()
            if self.reader.name() != 'Item':
                break
            widget.addItem(self.set_vars(self.reader.readElementText()))
        widget.setCurrentIndex(index)

    # 签名框
    def signBox(self):
        widget = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.boxresize(widget)
        widget.setEnabled(False)
        widget.setStyleSheet("background-color: rgb(255, 0, 0);")
        widget.setText(self.reader.readElementText(1))

    # 表达式
    def exprBox(self):
        widget = QtWidgets.QLineEdit(self.scrollAreaWidgetContents)
        self.boxresize(widget)
        widget.setEnabled(False)
        widget.setStyleSheet("background-color: rgb(85, 255, 255);")
        # style = self.reader.attributes().value("showformat")
        # 后缀
        sibfix = ''
        # 计算过程
        expr = ''
        # 显示的表达式
        va = ''
        vid = self.reader.attributes().value("ID")
        while 1:
            self.reader.readNextStartElement()
            if self.reader.isEndElement() and self.reader.name() == "Expr":
                break
            if self.reader.name() == "subfix":
                sibfix = self.reader.readElementText()
            elif self.reader.name() == "expr":
                expr = self.reader.readElementText()
            elif self.reader.name() == "vars":
                va = self.reader.readElementText()

        # 把文件中的#变量，改为实例中的变量。
        expr = expr.replace('#', 'self.')
        expr = self.set_vars(expr)
        va = self.set_vars(va)

        try:
            result = str(eval(expr, evalenv(self)))
            widget.setText(va + result + sibfix)
            if id:
                setattr(self, id, decimal.Decimal(result))
        except:
            return "公式格式错误"
        # widget.setText(self.reader.readElementText(1))
        if vid:
            setattr(self, vid, result)

    # 换行框
    def wrapBox(self):
        self.current_X = 20
        self.current_Y += 20

    # 设置控件的尺寸
    # w:控件的宽度变量名
    # h:控件的高度变量名
    def boxresize(self, widget, w="width", h="height"):
        self.setStyleSheet("margin:2 2;")
        width = int(self.reader.attributes().value(
            w)) * 7 + 4 if self.reader.attributes().value(
            w) else 134
        height = int(self.reader.attributes().value(
            h)) * 24 if self.reader.attributes().value(
            h) else 24
        widget.resize(width, height)
        widget.move(self.current_X, self.current_Y)
        self.current_X += width

    # 设置表达式
    def set_vars(self, exp):
        items, sys_items = self.get_vars(exp)
        if items:
            for item in set(items):
                try:
                    exp = exp.replace(item, str(getattr(self, item[1:-1])))
                except AttributeError:
                    exp = exp.replace(item, '')
        if sys_items:
            for item in set(sys_items):
                try:
                    # 切片去除头尾的@
                    # 日期类变量
                    if item[1: -1] in (
                    'NIAN', 'YUE', 'RI', 'SHI', 'FEN', 'MIAO'):
                        exp = exp.replace(item,
                                          str(getattr(userdetail, item[1:-1])))
                    # 产品信息类变量
                    elif item[1: -1] in PRODUCT_DICT:
                        if self.proddetail is not None:
                            exp = exp.replace(item, str(
                                self.proddetail[PRODUCT_DICT[item[1: -1]]]))
                        else:
                            try:
                                self.get_sys_vars(0)
                                exp = exp.replace(item, str(
                                    self.proddetail[PRODUCT_DICT[item[1: -1]]]))
                            except IndexError:
                                exp = exp.replace(item, str(''))
                    # 产品物料，分批次
                    elif item[3: -2] in STUFF_DICT or item[3: -3] in STUFF_DICT:
                        # 变量的后缀
                        num = int(re.search(r'\d+', item).group(0)) - 1
                        vals = [x for x in re.split(r'@|\d', item) if x][0]
                        var_list = getattr(self, 'stuffdetail' + item[1: 3])
                        if len(var_list):
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[2:]])))
                        else:
                            self.get_sys_vars(1)
                            var_list = getattr(self, 'stuffdetail' + item[1: 3])
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[2:]])))
                    # 产品物料，不分批次
                    elif item[4: -2] in STUFF_DICT or item[4: -3] in STUFF_DICT:
                        # 变量的后缀
                        num = int(re.search(r'\d+', item).group(0)) - 1
                        vals = [x for x in re.split(r'@|\d', item) if x][0]
                        var_list = getattr(self, 'stuffdetail' + item[1: 4])
                        if len(var_list):
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[3:]])))
                        else:
                            self.get_sys_vars(2)
                            var_list = getattr(self, 'stuffdetail' + item[1: 4])
                            exp = exp.replace(item, str(
                                getattr(var_list[num], STUFF_DICT[vals[3:]])))
                    # 检验报告类信息变量
                    elif item[1: -1] in LAB_DICT:
                        if self.labdetail is not None:
                            exp = exp.replace(item, str(
                                self.labdetail[LAB_DICT[item[1: -1]]]))
                        else:
                            self.get_sys_vars(3)
                            exp = exp.replace(item, str(
                                self.labdetail[LAB_DICT[item[1: -1]]]))
                except:
                    exp = exp.replace(item, str(''))
        return exp

    # 获取系统变量的值
    # kind  获取的数据类型，0生产，1物料，2检验
    def get_sys_vars(self, kind=0):
        if self.autoid != 0:
            try:
                if kind == 0:
                    pm = ProductController()
                    self.proddetail = pm.get_producingplan(autoid=self.autoid)[
                        0]
                elif kind == 1:
                    sm = StuffController()
                    self.stuffdetail = sm.get_prodstuff(self.autoid)
                    for item in self.stuffdetail:
                        stufftype = item.stufftype
                        if stufftype == 0:
                            self.stuffdetailZC.append(item)
                            self.stuffdetailZF.append(item)
                        elif stufftype == 1:
                            self.stuffdetailFC.append(item)
                            self.stuffdetailZF.append(item)
                        elif stufftype == 2:
                            self.stuffdetailNB.append(item)
                            self.stuffdetailBC.append(item)
                        elif stufftype == 3:
                            self.stuffdetailWB.append(item)
                            self.stuffdetailBC.append(item)
                        elif stufftype == 4:
                            self.stuffdetailQC.append(item)
                elif kind == 2:
                    sm = StuffController()
                    self.mstuffdetail = sm.get_Mprodstuff(self.autoid)
                    for item in self.mstuffdetail:
                        stufftype = item.stufftype
                        if stufftype == 0:
                            self.stuffdetailMZC.append(item)
                            self.stuffdetailMZF.append(item)
                        elif stufftype == 1:
                            self.stuffdetailMFC.append(item)
                            self.stuffdetailMZF.append(item)
                        elif stufftype == 2:
                            self.stuffdetailMNB.append(item)
                            self.stuffdetailMBC.append(item)
                        elif stufftype == 3:
                            self.stuffdetailMWB.append(item)
                            self.stuffdetailMBC.append(item)
                        elif stufftype == 4:
                            self.stuffdetailMQC.append(item)
                elif kind == 3:
                    lm = LabrecordsController()
                    self.labdetail = lm.get_labrecord(1, autoid=self.autoid)[0]
            except:
                # traceback.print_exc()
                pass

    # 获得表达式中的普通变量和系统变量
    # {\w*} 普通变量
    # @\w*@ 系统变量
    def get_vars(self, exp):
        pattern1 = re.compile(r'{\w*}')
        pattern2 = re.compile(r'@\w*@')
        return pattern1.findall(exp), pattern2.findall(exp)

    '''
    def paintEvent(self, event):
        if self.line_border:
            #self.pix = self.pix.scaled(self.size())
            pp = QtGui.QPainter(self)
            #pp = QtGui.QPainter(self.pix)
            pen = QtGui.QPen()  # 定义笔格式对象
            for index, item in enumerate(self.line_border):
                print(item)
                pen.setWidth(item[1])  # 设置笔的宽度
                pen.setColor(QtCore.Qt.red)
                pp.setPen(pen)  # 将笔格式赋值给 画笔
                # 根据鼠标指针前后两个位置绘制直线
                pp.drawRect(item[0])
                #self.line_border.pop(index)

            #painter = QtGui.QPainter(self)
            # 在画布上画出
            #painter.drawPixmap(0, 0, self.pix)
    '''

    def widgetedit(self):
        widget = self.sender().objectName()
        # s = self.writer.setQuery("GMPPaper/Title[2]")
        # for item in s:
        #    print(s)
        # num = widget[6:]
        # self.writer.writeCurrentToken()
        # print(self.reader.namespaceUri())


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainmenu = ReadXML()

    res = Selfdefinedformat.objects.filter(autoid=2855)
    mainmenu.__setattr__('autoid', 50)
    mainmenu.read(res[0].format)
    mainmenu.show()
    sys.exit(app.exec_())
