# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog, QTreeWidgetItem, QTreeWidgetItemIterator, \
    QMenu
from PyQt5.QtGui import QBrush, QColor
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QPoint, QTimer

from stuff.controllers.stuffcontroller import StuffController

from productline.controllers.productlineconroller import ProductLineConroller
from product.controllers.productcontroller import ProductController
from warehouse.controllers.warehousecontroller import WarehouseController
from warehouse.modules.modifydrawamountmodule import ModifyDrawamountModule
from warehouse.views.drawstuff import Ui_Dialog

from lib.utils.evalenv import evalenv, rnd
from lib.utils.saveexcept import SaveExcept
from lib.utils.messagebox import MessageBox

from decimal import Decimal

import re

import user

STUFFTYPE = ("主材料", "前处理", "辅材料", "内包材", "外包材")
VAR_ITEM = {'计划量': 'presamount', "实际量": 'pracamount', "领用量": 'drawamount'}


class DrawstuffModule(QDialog, Ui_Dialog):

    def __init__(self, ppid, sdpid, kind, parent=None):
        super(DrawstuffModule, self).__init__(parent)
        self.ppid = ppid
        self.sdpid = sdpid
        self.kind = kind
        self.setupUi(self)
        self.WC = WarehouseController()
        self.SC = StuffController()
        self.PC = ProductController()
        self.PLC = ProductLineConroller()
        self.detail = dict()
        self.stuff_list = []
        # 当前正在修改的树节点
        self.edittreeitem = None
        self.stuff_repository = []
        # 公式错误信息
        self.errormsg = []
        self.treeWidget_stuffrepository.setDragDropMode(1)
        self.treeWidget_drawstuff.setDragDropMode(2)

    def showMaximized(self):
        try:
            # 获取产品信息
            self.get_product_detail()
            self.get_formula()
            self.get_has_drawstuff(self.ppid)
            self.draw_stuff()
            # 配方有错误信息，提示错误内容
            if len(self.errormsg):
                self.pushButton_accept.setEnabled(False)
                self.show_errormsg(self.errormsg)
            super(DrawstuffModule, self).showMaximized()
        except Exception as e:
            self.done(6)

    # 显示错误信息
    def show_errormsg(self, msg):
        text = "以下物料配方设置出错，请检查配方后重新领料"
        informative = ""
        for i, item in enumerate(msg):
            informative += str(i+1) + '、' + item + '设置出错\n'
        dialog = MessageBox(self, text=text, informative=informative)
        dialog.show()

    # 获取当前领料单的物料配方
    def get_formula(self):
        # 获得配方
        if self.kind == 0:
            res = self.PLC.get_formula(
                prodid=self.detail['prodid'], version=self.detail['version'],
                stufftype__in=(0, 1)
            )
        else:
            res = self.PLC.get_formula(
                prodid=self.detail['prodid'], version=self.detail['version'],
                stufftype=self.kind + 1
            )
        stuffkind_list = []
        if len(res):
            # 显示配方
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_formula)
                qtreeitem.setText(1, STUFFTYPE[item.stufftype])
                qtreeitem.setText(2, item.stuffkind)
                qtreeitem.setText(3, item.formula)
                qtreeitem.setText(4, item.presexpression)
                qtreeitem.setText(5, item.pracexpression)
                qtreeitem.setText(6, item.drawexpression)
                # 领料精度
                qtreeitem.setText(7, str(item.precision))
                # 损耗限度
                qtreeitem.setText(8, str(item.loss))
                # 标记该物料是否已经发够料
                qtreeitem.setText(9, '0')
                stuffkind_list.append(item.stuffkind)

            self.treeWidget_formula.hideColumns(0, 4, 5, 6, 7, 8, 9)
            self.treeWidget_formula.resizeColumns(300, 1, 2, 3)
        # 如果当前配方不为空，则获取对应的库存
        if len(stuffkind_list):
            self.get_stuffrep_gt_zero(stuffkind_list)

    # 获取本批产品其他领料单已经领取了的物料
    def get_has_drawstuff(self, ppid):
        values_tupe = (
            "autoid", "stuffid", "stuffname", "stuffkind", "spec", "package",
            "presamount", "pracamount", "drawamount", "content", "water",
            "impurity", "rdensity"
        )
        stuffs = self.SC.get_prodstuff(0, ppid=ppid, *values_tupe)
        if len(stuffs):
            self.stuff_list_additem(stuffs)

    # 把领取的物料加到领料记录中，如果发现重复的情况则替换旧的记录
    def stuff_list_additem(self, newitems):
        for newitem in newitems:
            flat = 0
            for item in self.stuff_list:
                if newitem['autoid'] == item['autoid']:
                    item = newitem
                    flat = 1
            if flat == 0:
                self.stuff_list.append(newitem)

    # 获取配方对应的物料
    def get_stuffrep_gt_zero(self, stuffkind_list):
        self.treeWidget_stuffrepository.clear()
        row_tuple = ('autoid', 'stuffkind', 'stuffid', 'stuffname', 'spec',
                     'package', 'batchno', 'mbatchno', 'amount', 'producer',
                     'supid', 'content', 'cunit', 'water', 'rdensity',
                     'impurity', 'basicunit', 'lrid', 'stufftype'
                     )
        res = self.WC.get_stuffrepository(1, *row_tuple,
                                          stuffkind__in=stuffkind_list,
                                          amount__gt=0)
        self.stuff_repository = res
        if len(res):
            for item in res:
                qtreeitem = QTreeWidgetItem(self.treeWidget_stuffrepository)
                qtreeitem.setText(0, str(item['autoid']))
                qtreeitem.setText(1, str(item['stuffkind']))
                qtreeitem.setText(2, item['stuffid'] + ' ' + item['stuffname'])
                qtreeitem.setText(3, item['spec'])
                qtreeitem.setText(4, item['package'])
                qtreeitem.setText(5, item['batchno'])
                qtreeitem.setText(6, item['mbatchno'])
                qtreeitem.setText(7, str(item['amount']) + item['basicunit'])
                qtreeitem.setText(9, item['supid'] + ' ' + item['supname'])
                qtreeitem.setText(10, item['producer'])
                qtreeitem.setText(11, str(item['content']) + item['cunit'])
                qtreeitem.setText(12, str(item['water']) + '%')
                qtreeitem.setText(13, str(item['rdensity']))
                qtreeitem.setText(14, str(item['impurity']))
            self.treeWidget_stuffrepository.hideColumns(0, 1, 15)
            column_list = [i for i in range(2, 15)]
            self.treeWidget_stuffrepository.resizeColumns(120, *column_list)

    # 获取产品信息
    def get_product_detail(self):
        vlist = (
            'prodid', 'version', 'planamount', 'realamount', 'spec',
            'basicamount', 'spamount', 'bpamount', 'bpamount'
        )
        res = self.PC.get_producingplan(1, *vlist, autoid=self.ppid)
        self.detail = res[0]

    # 系统根据配方自动领料
    def draw_stuff(self):
        it = QTreeWidgetItemIterator(self.treeWidget_formula)
        while it.value():
            item = it.value()
            # 标记为0的列即为未领够料的记录
            if item.text(9) == '0':
                stuffkind = item.text(2)
                precision = int(item.text(7))
                loss = item.text(8)
                # 处理产品信息的变量,去除系统变量
                item.setText(4, self.reckon_expression(item.text(4), 1))
                # 计划量
                try:
                    presamount = Decimal(rnd(eval(item.text(4), evalenv(self)),
                                             precision))
                except SyntaxError:
                    if stuffkind+' 计划量' not in self.errormsg:
                        self.errormsg.append(stuffkind + ' 计划量')
                    presamount = 0

                # 把计划量加到产品信息变量中
                # self.detail['presamount'] = presamount
                # 实际量公式,去除系统变量
                item.setText(5, self.reckon_expression(item.text(5), 1))
                # 领取量公式,去除系统变量
                item.setText(6, self.reckon_expression(item.text(6), 1))
                # 计算领料量,返回领料情况res, 和标记：是否已经领购料
                res = self.reckon_drawamount(
                    stuffkind, presamount, precision, item.text(5),
                    item.text(6), loss
                )
                if len(res):
                    self.treeWidget_drawstuff_add_item(res)
            it += 1
        self.is_drawamount_enough()

    # 把计算结果存到领料树中
    def treeWidget_drawstuff_add_item(self, items: dict):
        try:
            self.stuff_list_additem(items)
            for item in items:
                qtreeitem = QTreeWidgetItem(self.treeWidget_drawstuff)
                qtreeitem.setText(0, str(item['autoid']))
                qtreeitem.setText(1, str(item['stuffkind']))
                qtreeitem.setText(2, item['stuffid'] + ' ' + item['stuffname'])
                qtreeitem.setText(3, item['spec'])
                qtreeitem.setText(4, item['package'])

                qtreeitem.setText(5, str(item['oripresamount']))
                qtreeitem.setText(6, item['basicunit'])

                qtreeitem.setText(7, str(item['newpracamount']))
                qtreeitem.setText(8, item['basicunit'])

                qtreeitem.setText(9, str(item['drawamount']))
                qtreeitem.setText(10, item['basicunit'])

                qtreeitem.setText(11, item['batchno'])
                qtreeitem.setText(12, item['mbatchno'])

                qtreeitem.setText(13, str(item['content']) + item['cunit'])
                qtreeitem.setText(14, str(item['water']) + '%')
                qtreeitem.setText(15, str(item['rdensity']))
                qtreeitem.setText(16, str(item['impurity']))
                qtreeitem.setText(17, str(item['loss']))

                qtreeitem.setText(18, item['supid'] + ' ' + item['supname'])
                qtreeitem.setText(19, item['producer'])

                qtreeitem.setText(20, str(item['presamount']))
                qtreeitem.setText(21, str(item['pracamount']))
                qtreeitem.setText(22, str(item['precision']))

                self.treeWidget_drawstuff.hideColumns(0, 1, 20, 21, 22)
                columns_list = [i for i in range(2, 20)]
                self.treeWidget_drawstuff.resizeColumns(200, *columns_list)
        except KeyError:
            pass

    # 计算系统变量
    def reckon_expression(self, expression, iterdepth):
        # iterdepth:迭代深度，超过50则抛出RuntimeError
        # 产品信息变量，ex: @planamount@, @spec@, @package@
        if iterdepth > 50:
            raise RuntimeError
        pattern = re.findall(r'@[%?!()（）:：.#\w]*@', expression)
        for item in pattern:
            if len(item[1:-1].split('.')) == 2:
                var_name, var_item = item[1:-1].split('.')
                value = Decimal('0')
                # 标记是否找到了对应的物料
                find_stuff_flag = 0
                for stuff in self.stuff_list:
                    if stuff['stuffkind'] == var_name:
                        find_stuff_flag = 1
                        if var_item == '计划量':
                            value = stuff[VAR_ITEM[var_item]]
                            expression = expression.replace(item, str(value))
                            break
                        else:
                            value += stuff[VAR_ITEM[var_item]]
                        expression = expression.replace(item, str(value))
                # 没有找到对应的物料则再本领料单中继续寻找
                if find_stuff_flag == 0:
                    formula_item = self.get_treeitem(self.treeWidget_formula)
                    while 1:
                        try:
                            treeitem = next(formula_item)
                            if treeitem.text(2) == var_name:
                                if treeitem.text(9) == '0':
                                    # stuffkind = item.text(2)
                                    precision = int(treeitem.text(7))
                                    loss = treeitem.text(8)
                                    # 处理产品信息的变量,去除系统变量
                                    treeitem.setText(4, self.reckon_expression(
                                        treeitem.text(4), iterdepth+1))
                                    # 计划量
                                    try:
                                        presamount = Decimal(
                                            rnd(eval(treeitem.text(4),
                                                     evalenv(self)), precision))
                                    except SyntaxError:
                                        if var_name + ' 计划量' not in self.errormsg:
                                            self.errormsg.append(var_name + ' 计划量')
                                        presamount = 0
                                    # 把计划量加到产品信息变量中
                                    # self.detail['presamount'] = presamount
                                    # 实际量公式,去除系统变量
                                    treeitem.setText(5, self.reckon_expression(
                                        treeitem.text(5), iterdepth+1))
                                    # 领取量公式,去除系统变量
                                    treeitem.setText(6, self.reckon_expression(
                                        treeitem.text(6), iterdepth+1))
                                    # 计算领料量,返回领料情况res, 和标记：是否已经领购料
                                    res = self.reckon_drawamount(
                                        var_name, presamount, precision,
                                        treeitem.text(5),
                                        treeitem.text(6), loss
                                    )
                                    if len(res):
                                        self.treeWidget_drawstuff_add_item(res)
                                        self.is_drawamount_enough()
                                        expression = self.reckon_expression(expression, iterdepth+1)
                        except (StopIteration, RuntimeError) as e:
                            break
            else:
                key = item.replace('@', '')
                if key in self.detail:
                    expression = expression.replace(item, str(self.detail[key]))
        #pattern_1 = re.findall(r'@[%?!()（）:：.#\w]*@', expression)
        return expression

    # 计算实际量
    def reckon_pracamount(self, autoid, presamount, precision, expression):
        # stuffkind: 物料种类
        # presamount: 计划量
        # expression: 实际量的公式
        stuff_detail = []
        # 最终要领取的批次和实际量
        # 分析公式，获取变量
        pattern = re.findall(r'@\w*@', expression)
        # 把变量设置为对应的值
        for item in self.stuff_repository:
            if autoid != item['autoid']:
                continue
            for key in pattern:
                k = key.replace('@', '')
                if k == 'presamount':
                    expression = expression.replace(key, str(presamount))
                elif k in item:
                    expression = expression.replace(key, str(item[k]))
                elif k in self.detail:
                    expression = expression.replace(key, str(self.detail[k]))
            try:
                pracamount = Decimal(rnd(eval(expression, evalenv(self)),
                                         precision))
            except SyntaxError:
                if item['stuffkind'] + ' 实际量' not in self.errormsg:
                    self.errormsg.append(item['stuffkind'] + ' 实际量')
                pracamount = 0
            item['pracamount'] = pracamount

    # 计算领取量
    def reckon_drawamount(self, stuffkindorsrid, presamount, precision,
                          prac_expression, draw_expression, loss=0, flat=True):
        # stuffkindorsrid: 根据flat决定类型， True是物料种类，False是srid
        # presamount: 计划量
        # precision: 计算结果精度
        # prac_expression: 实际量公式
        # draw_expression: 领取公式
        # loss: 损耗限度
        # flat: 是否需要继续领下一批物料，默认为True即继续领下一批物料,
        #       False则不再领取下一批物料

        # 要领取的物料批次
        draw_list = []
        # 已经领取了的量
        has_drawamount = 0
        # 分析公式，获取变量
        pattern = re.findall(r'@\w*@', draw_expression)
        # 把变量设置为对应的值
        for item in self.stuff_repository:

            item['oripresamount'] = presamount
            new_expression = draw_expression
            if has_drawamount != 0:
                presamount -= has_drawamount
                has_drawamount = 0
            if stuffkindorsrid != (
                    item['stuffkind'] if flat else str(item['autoid'])):
                continue
            has_draw_stuff = self.get_treeitem(self.treeWidget_drawstuff)
            # 检查该批次是否已经选择过了
            draw_flag = 0
            while 1:
                try:
                    stuff = next(has_draw_stuff)
                    if int(stuff.text(0)) == item['autoid']:
                        draw_flag = 1
                        break
                except StopIteration:
                    break
            if draw_flag == 1:
                continue
            item['loss'] = loss
            item['presamount'] = presamount
            item['precision'] = precision
            # 算出该批次对应的实际量
            self.reckon_pracamount(item['autoid'], presamount, precision,
                                   prac_expression)
            for key in pattern:

                k = key.replace('@', '')
                if k in item:
                    new_expression = new_expression.replace(key, str(item[k]))
                elif k in self.detail:
                    new_expression = new_expression.replace(key, str(
                        self.detail[k]))
            try:
                drawamount = Decimal(rnd(eval(new_expression, evalenv(self)),
                                         precision))
            except SyntaxError:
                if stuffkindorsrid + ' 领取量' not in self.errormsg:
                    self.errormsg.append(stuffkindorsrid + ' 领取量')
                drawamount = 0
            if drawamount == 0:
                continue
            elif item['amount'] >= drawamount:
                item['drawamount'] = drawamount
                item['newpracamount'] = item['pracamount']
                draw_list.append(item)
                break
            else:
                # 转化为计划量 = 领取量 * 计划量 / 实际量
                has_drawamount = Decimal(
                    rnd(item['amount'] * presamount / item['pracamount'],
                        precision))
                item['newpracamount'] = rnd(item['amount'], precision)
                item['drawamount'] = rnd(item['amount'], precision)
                draw_list.append(item)
                if not flat:
                    # 指定库存记录时，默认按领够料处理
                    break
        return draw_list

    # 配方点击功能，选择一个物料种类后库存列表中只显示该物料
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_formula_itemClicked(self, qtreeitem, p_int):
        stuffkind_list = [qtreeitem.text(2)]
        self.get_stuffrep_gt_zero(stuffkind_list)

    # 拖动库存记录到领料表
    @pyqtSlot(str)
    def on_treeWidget_drawstuff_droped(self, p_str):
        try:
            srid = int(p_str)
            # 如果该批次物料已经有领料记录则不做任何操作
            if self.has_drawstuff(p_str):
                return
            stuff = dict()
            for item in self.stuff_repository:
                if srid == item['autoid']:
                    stuff = item
                    break
            if stuff is None:
                raise KeyError
            stuffkind = stuff['stuffkind']
            it_formula = self.get_treeitem(self.treeWidget_formula)

            while 1:
                try:
                    treeitem = next(it_formula)
                    if treeitem.text(2) == stuffkind:
                        planamount_expression = treeitem.text(4)
                        pracamount_expression = treeitem.text(5)
                        drawamount_expression = treeitem.text(6)
                        precision = int(treeitem.text(7))
                        loss = treeitem.text(8)
                        try:
                            presamount = Decimal(rnd(eval(planamount_expression,
                                                          evalenv(self)),
                                                     precision))
                        except SyntaxError:
                            if stuffkind + ' 计划量' not in self.errormsg:
                                self.errormsg.append(stuffkind + ' 计划量')
                            presamount = 0
                        # 没有领够料，继续拖新的物料批次
                        if treeitem.text(9) == '0':
                            # 获取出该物料其他批次的实际领取量
                            it_drawstuff = self.get_treeitem(
                                self.treeWidget_drawstuff)
                            try:
                                new_presamount = presamount
                                while 1:
                                    drawitem = next(it_drawstuff)
                                    if drawitem.text(1) != stuffkind:
                                        continue
                                    # 转化为计划量 = 领取量 * 计划量 / 实际量
                                    has_drawamount = rnd(
                                        Decimal(drawitem.text(9)) * Decimal(
                                            drawitem.text(20)) / Decimal(
                                            drawitem.text(21)),
                                        int(drawitem.text(22)))
                                    new_presamount -= has_drawamount
                            except StopIteration:
                                pass
                            # 计算本批的领取量
                            res = self.reckon_drawamount(
                                p_str, new_presamount, precision,
                                pracamount_expression,
                                drawamount_expression, loss, False
                            )
                        # 已经领够料，还继续拖新的物料批次
                        elif treeitem.text(9) == '1':
                            res = self.reckon_drawamount(
                                p_str, presamount, precision,
                                pracamount_expression, drawamount_expression,
                                loss, False
                            )
                        if len(res):
                            res[0]['oripresamount'] = presamount
                            self.treeWidget_drawstuff_add_item(res)
                        self.is_drawamount_enough()
                        break
                except StopIteration:
                    break
        except ValueError:
            SaveExcept(ValueError, "拖动库存信息时出错,传入的不是srid", p_str,
                       self.stuff_repository)
        except KeyError:
            SaveExcept(ValueError, "拖动库存信息时出错,没有找到对应的库存记录,", p_str,
                       self.stuff_repository)

    # 领够料的物料自动设置成绿色，不够料的物料设置成黄色
    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_formula_itemChanged(self, qtreeitem, p_int):
        if p_int == 9:
            brush = QBrush(1)
            if qtreeitem.text(9) == '1':
                brush.setColor(QColor(85, 255, 127))
            else:
                brush.setColor(QColor(255, 255, 127))
            for i in range(1, 4):
                qtreeitem.setBackground(i, brush)

    @pyqtSlot(QTreeWidgetItem, int)
    def on_treeWidget_drawstuff_itemDoubleClicked(self, qtreeitem, p_int):
        try:
            srid = int(qtreeitem.text(0))
            srdetail = dict()
            for item in self.stuff_repository:
                if item['autoid'] == srid:
                    srdetail = item
                    break
            dialog = ModifyDrawamountModule(srdetail, self)
            self.edittreeitem = qtreeitem
            dialog.modified.connect(self.setdrawamount)
            dialog.exec()
        except ValueError:
            pass

    # 把领料量设置为新的值
    def setdrawamount(self, q_decimal):
        stuffkind = ''
        self.edittreeitem.setText(9, str(q_decimal))
        self.edittreeitem.setText(7, str(q_decimal))
        srid = int(self.edittreeitem.text(0))
        for item in self.stuff_repository:
            if item['autoid'] == srid:
                item['pracamount'] = q_decimal
                item['drawamount'] = q_decimal
                stuffkind = item['stuffkind']
                break
        self.is_drawamount_enough()
        self.edittreeitem = None

    # 判断领取的物料是否足够
    def is_drawamount_enough(self):
        formula_treeitem = self.get_treeitem(self.treeWidget_formula)

        while 1:
            presamount = Decimal('0')
            try:
                fitem = next(formula_treeitem)
                precision = int(fitem.text(7))
                presamount = Decimal(rnd(
                    eval(fitem.text(4), evalenv(self)), precision)
                )
                stuffkind = fitem.text(2)
                drawstuff_treeitem = self.get_treeitem(
                    self.treeWidget_drawstuff)
                while 1:
                    try:
                        ditem = next(drawstuff_treeitem)
                        if ditem.text(1) != stuffkind:
                            continue
                        this_presamount = rnd(
                            Decimal(ditem.text(7)) * Decimal(ditem.text(20)) /
                            Decimal(ditem.text(21)), precision
                        )
                        presamount -= this_presamount
                    except StopIteration:
                        break
                if presamount > 0:
                    fitem.setText(9, '0')
                else:
                    fitem.setText(9, '1')

            except StopIteration:
                break
            except SyntaxError:
                continue

    # 删除已经选择好了的物料
    @pyqtSlot(QPoint)
    def on_treeWidget_drawstuff_customContextMenuRequested(self, pos):
        sender_widget = self.sender()
        menu = QMenu()
        button1 = menu.addAction("删除该批次物料")
        button2 = menu.addAction("修改领取量")
        global_pos = sender_widget.mapToGlobal(pos)
        action = menu.exec(global_pos)
        # 删除该批次物料
        if action == button1:
            try:
                self.delete_drawstuff(sender_widget.selectedItems())
            except AttributeError:
                pass
        # 修改领取量
        elif action == button2:
            try:
                self.modify_drawstuff(sender_widget.currentItem())
            except AttributeError:
                pass

    # 判断物料是否已经有领取记录
    def has_drawstuff(self, p_str):
        itemiter = self.get_treeitem(self.treeWidget_drawstuff)
        flag = False
        while 1:
            try:
                treeitem = next(itemiter)
                if p_str == treeitem.text(0):
                    flag = True
                    break
            except StopIteration:
                break
        return flag

    # 删除待领取的物料
    def delete_drawstuff(self, qtreeitems):
        # qtreeitems： 选中的项目
        if len(qtreeitems):
            it = QTreeWidgetItemIterator(self.treeWidget_formula)
            root = self.treeWidget_drawstuff.invisibleRootItem()
            for item in qtreeitems:
                root.removeChild(item)
            self.is_drawamount_enough()

    def get_treeitem(self, qtreewidget):
        it = QTreeWidgetItemIterator(qtreewidget)
        while it.value():
            yield it.value()
            it += 1

    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        it = QTreeWidgetItemIterator(self.treeWidget_drawstuff)
        draw_list = []
        key_list = ['srid', 'stuffkind']
        while it.value():
            treeitem = it.value()
            item = self.qtreeitem2dict(key_list, treeitem)
            for stuff in self.stuff_repository:
                if stuff['autoid'] == int(item['srid']):
                    item['stuffid'] = stuff['stuffid']
                    item['stuffname'] = stuff['stuffname']
                    item['stufftype'] = stuff['stufftype']
                    item['stuffkind'] = stuff['stuffkind']
                    item['spec'] = stuff['spec']
                    item['package'] = stuff['package']
                    item['producer'] = stuff['producer']
                    item['batchno'] = stuff['batchno']
                    item['lrid'] = stuff['lrid']
                    item['content'] = stuff['content']
                    item['cunit'] = stuff['cunit']
                    item['water'] = stuff['water']

                    item['impurity'] = stuff['impurity']
                    item['rdensity'] = stuff['rdensity']
                    item['mbatchno'] = stuff['mbatchno']
                    break
            item['sdpid'] = self.sdpid
            item['ppid'] = self.ppid
            draw_list.append(item)
            it += 1
        sdpid_list = {
            'autoid': self.sdpid,
            'status': 2,
            'providerid': user.user_id,
            'providername': user.user_name,
            'drawtime': user.time
        }
        res = self.WC.update_stuffrepository_amount(*draw_list, **sdpid_list)
        print(res)
        if res == 'accept':
            self.accept()
        elif res == 'rollback':
            msg = MessageBox(parent=self, text="领料信息异常！", informative="请刷新后重试!")
            msg.show()
            timer = QTimer(self)
            timer.start(1000)
            timer.timeout.connect(msg.close)

    def qtreeitem2dict(self, key_list: list, q_treeitem: QTreeWidgetItem):
        q_dict = dict()
        q_dict['srid'] = q_treeitem.text(0)
        q_dict['presamount'] = Decimal(q_treeitem.text(5))
        q_dict['checkamount'] = Decimal(q_treeitem.text(5))
        q_dict['presunit'] = q_treeitem.text(6)
        q_dict['pracamount'] = Decimal(q_treeitem.text(7))
        q_dict['pracunit'] = q_treeitem.text(8)
        q_dict['drawamount'] = Decimal(q_treeitem.text(9))
        q_dict['drawunit'] = q_treeitem.text(10)
        q_dict['loss'] = q_treeitem.text(17)
        q_dict['precision'] = int(q_treeitem.text(22))
        return q_dict

    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()