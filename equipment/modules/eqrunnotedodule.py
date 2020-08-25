# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import QDialog
from PyQt5 .QtGui import QRegExpValidator
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QDateTime, QRegExp

from equipment.controllers.equipmentcontroller import EquipmentController
from equipment.views.eqrunnote import Ui_Dialog

import datetime

import user


class EqrunnoteModule(QDialog, Ui_Dialog):
    flush_signal = pyqtSignal()

    def __init__(self, autoid, starttime=user.currentdatetime, endtime=user.currentdatetime, parent=None):
        super(EqrunnoteModule, self).__init__(parent)

        self.autoid = autoid
        self.starttime = starttime
        self.endtime = endtime
        self.setupUi(self)
        self.maintenance = bin(0)
        self.ori_detail = object
        self.new_detail = {}
        self.EC = EquipmentController()
        # 获取记录详细内容
        self.get_eq_run_note_detail(autoid)
        reg = QRegExp('^[0-9]+$')
        self.lineEdit_runtime_day.setValidator(QRegExpValidator(reg))
        self.lineEdit_runtime_hour.setValidator(QRegExpValidator(reg))
        self.lineEdit_runtime_minute.setValidator(QRegExpValidator(reg))

    # 获取详细运行记录
    def get_eq_run_note_detail(self, autoid):
        res = self.EC.get_equip_run_note(autoid)
        if len(res):
            self.ori_detail = res[0]
            self.label_equipment.setText(
                self.ori_detail.eqno + ' ' + self.ori_detail.eqname)
            self.lineEdit_product.setText(
                self.ori_detail.dictid + ' ' + self.ori_detail.dictname)
            self.lineEdit_batchno.setText(self.ori_detail.batchno)
            if type(self.ori_detail.runstarttime) is datetime.datetime:
                self.dateTimeEdit_runstarttime.setDateTime(
                    self.ori_detail.runstarttime)
            else:
                self.dateTimeEdit_runstarttime.setDateTime(self.starttime())
            if type(self.ori_detail.runendtime) is datetime.datetime:
                self.dateTimeEdit_runendtime.setDateTime(self.ori_detail.runendtime)
            else:
                self.dateTimeEdit_runendtime.setDateTime(self.endtime())
            self.set_runtime(self.ori_detail.runtime)
            self.comboBox_runstatus.setCurrentIndex(
                int(self.ori_detail.runstatus))
            self.lineEdit_remark.setText(self.ori_detail.remark)
            if self.ori_detail.fillerid and self.ori_detail.fillername:
                self.pushButton_filler.setText(self.ori_detail.fillerid + ' ' + self.ori_detail.fillername)
            self.comboBox_startstatus.setCurrentIndex(
                int(self.ori_detail.startstatus))
            self.comboBox_stopstatus.setCurrentIndex(
                int(self.ori_detail.stopstatus))
            self.maintenance = self.ori_detail.maintenance
            bin_list = bin(self.ori_detail.maintenance)[2:]
            for i in range(1, len(bin(self.ori_detail.maintenance)[2:]) + 1):
                try:
                    getattr(self, "checkBox_" + str(i)).setChecked(
                        int(bin_list[-i]))
                except IndexError:
                    break

    # 修改开始运行时间
    @pyqtSlot(QDateTime)
    def on_dateTimeEdit_runstarttime_dateTimeChanged(self, qdtime):
        if qdtime.isValid():
            try:
                if qdtime != self.ori_detail.runstarttime:
                    self.new_detail['runstarttime'] = qdtime.toPyDateTime()
                    #'yyyy-MM-dd hh:mm:ss')
                    runtime = int((
                                              self.dateTimeEdit_runendtime.dateTime().toSecsSinceEpoch() - qdtime.toSecsSinceEpoch()) / 60)
                    self.set_runtime(runtime)
                    self.new_detail['runtime'] = runtime
                else:
                    try:
                        del self.new_detail['runstarttime']
                    except KeyError:
                        pass

            except AttributeError:
                self.new_detail['runstarttime'] = qdtime

    # 修改结束运行时间
    @pyqtSlot(QDateTime)
    def on_dateTimeEdit_runendtime_dateTimeChanged(self, qdtime):
        if qdtime.isValid():
            try:
                if qdtime != self.ori_detail.runendtime:
                    self.new_detail['runendtime'] = qdtime.toPyDateTime()
                    self.new_detail['runendtime'] = datetime.datetime.now()
                    runtime = int((
                                              qdtime.toSecsSinceEpoch() - self.dateTimeEdit_runstarttime.dateTime().toSecsSinceEpoch()) / 60)
                    self.set_runtime(runtime)
                    self.new_detail['runtime'] = runtime
                else:
                    try:
                        del self.new_detail['runendtime']
                    except KeyError:
                        pass

            except AttributeError:
                self.new_detail['runendtime'] = qdtime

    # 修改运行时长-day
    @pyqtSlot(str)
    def on_lineEdit_runtime_day_textEdited(self, p_str):
        self.modify_runtime()

    # 修改运行时长-hour
    @pyqtSlot(str)
    def on_lineEdit_runtime_hour_textEdited(self, p_str):
        self.modify_runtime()

    # 修改运行时长-minute
    @pyqtSlot(str)
    def on_lineEdit_runtime_minute_textEdited(self, p_str):
        self.modify_runtime()

    # 修改运行时长
    def modify_runtime(self):
        day = int(self.lineEdit_runtime_day.text()) if self.lineEdit_runtime_day.text() else 0
        hour = int(self.lineEdit_runtime_hour.text()) if self.lineEdit_runtime_hour.text() else 0
        minute = int(self.lineEdit_runtime_minute.text()) if self.lineEdit_runtime_minute.text() else 0

        try:
            runtime = day * 86400 + hour*3600 + minute * 60
            if runtime != self.ori_detail.runtime:
                self.new_detail['runtime'] = runtime
            else:
                try:
                    del self.new_detail['runtime']
                except KeyError:
                    pass
            self.dateTimeEdit_runendtime.setDateTime(QDateTime.fromSecsSinceEpoch(self.dateTimeEdit_runstarttime.dateTime().toSecsSinceEpoch() + runtime))
        except ValueError:
            pass
        except AttributeError:
            self.new_detail['runtime'] = runtime

    # 修改运行情况
    @pyqtSlot(int)
    def on_comboBox_runstatus_currentIndexChanged(self, p_int):
        try:
            if p_int != self.ori_detail.runstatus:
                self.new_detail['runstatus'] = p_int
            else:
                try:
                    del self.new_detail['runstatus']
                except KeyError:
                    pass
        except ValueError:
            pass
        except AttributeError:
            self.new_detail['runstatus'] = p_int

    # 修改开机准备
    @pyqtSlot(int)
    def on_comboBox_startstatus_currentIndexChanged(self, p_int):
        try:
            if p_int != self.ori_detail.startstatus:
                self.new_detail['startstatus'] = p_int
            else:
                try:
                    del self.new_detail['startstatus']
                except KeyError:
                    pass
        except ValueError:
            pass
        except AttributeError:
            self.new_detail['startstatus'] = p_int

    # 修改停机保养
    @pyqtSlot(int)
    def on_comboBox_stopstatus_currentIndexChanged(self, p_int):
        try:
            if p_int != self.ori_detail.stopstatus:
                self.new_detail['stopstatus'] = p_int
            else:
                try:
                    del self.new_detail['stopstatus']
                except KeyError:
                    pass
        except ValueError:
            pass
        except AttributeError:
            self.new_detail['stopstatus'] = p_int

    # 修改备注
    @pyqtSlot(str)
    def on_lineEdit_remark_textEdited(self, p_str):
        try:
            if p_str != self.ori_detail.remark:
                self.new_detail['remark'] = p_str
            else:
                try:
                    del self.new_detail['remark']
                except KeyError:
                    pass
        except ValueError:
            pass
        except AttributeError:
            self.new_detail['remark'] = p_str

    # 修改填写人
    @pyqtSlot(str)
    def on_pushButton_filler_signChanged(self, p_str):
        try:
            fillerid, fillername = p_str.split(' ') if p_str else ('', '')
            if fillerid != self.ori_detail.fillerid and fillername != self.ori_detail.fillername:
                self.new_detail['fillerid'] = fillerid
                self.new_detail['fillername'] = fillername
            else:
                try:
                    del self.new_detail['fillerid']
                    del self.new_detail['fillername']
                except KeyError:
                    pass
        except ValueError:
            pass
        except AttributeError:
            self.new_detail['fillerid'] = fillerid
            self.new_detail['fillername'] = fillername

    @pyqtSlot(bool)
    def on_checkBox_1_clicked(self, p_int):
        self.set_maintenance(1, p_int)

    @pyqtSlot(bool)
    def on_checkBox_2_clicked(self, p_int):
        self.set_maintenance(2, p_int)

    @pyqtSlot(bool)
    def on_checkBox_3_clicked(self, p_int):
        self.set_maintenance(3, p_int)

    @pyqtSlot(bool)
    def on_checkBox_4_clicked(self, p_int):
        self.set_maintenance(4, p_int)

    @pyqtSlot(bool)
    def on_checkBox_5_clicked(self, p_int):
        self.set_maintenance(5, p_int)

    @pyqtSlot(bool)
    def on_checkBox_6_clicked(self, p_int):
        self.set_maintenance(6, p_int)

    @pyqtSlot(bool)
    def on_checkBox_7_clicked(self, p_int):
        self.set_maintenance(7, p_int)

    @pyqtSlot(bool)
    def on_checkBox_8_clicked(self, p_int):
        self.set_maintenance(8, p_int)

    @pyqtSlot(bool)
    def on_checkBox_9_clicked(self, p_int):
        self.set_maintenance(9, p_int)

    @pyqtSlot(bool)
    def on_checkBox_10_clicked(self, p_int):
        self.set_maintenance(10, p_int)

    # 设置设备状态
    # pos:第几个位置
    # status:该位置的值
    def set_maintenance(self, pos, status):
        values = 2 ** (pos - 1) * (1 if status else -1)
        self.maintenance += values
        try:
            if self.maintenance != self.ori_detail.maintenance:
                self.new_detail['maintenance'] = self.maintenance
            else:
                try:
                    del self.new_detail['maintenance']
                except KeyError:
                    pass
        except ValueError:
            pass
        except AttributeError:
            self.new_detail['maintenance'] = self.maintenance

    # 确认
    @pyqtSlot()
    def on_pushButton_accept_clicked(self):
        if len(self.new_detail):
            res = self.EC.update_equip_run_note(self.autoid, **self.new_detail)
            if res:
                self.flush_signal.emit()
                self.close()

    # 取消
    @pyqtSlot()
    def on_pushButton_cancel_clicked(self):
        self.close()

    # 把整数转为天-时-分
    def set_runtime(self, p_int: int):

        day = int(p_int / 1440)
        hour = (p_int % 1440 // 60) if p_int > 0 else int(p_int % -1440 / 60)
        minute = p_int % (60 if p_int > 0 else -60)
        self.lineEdit_runtime_day.setText(str(day))
        self.lineEdit_runtime_hour.setText(str(hour))
        self.lineEdit_runtime_minute.setText(str(minute))


RUN_STATUS = ("正常运行", "停用待修", "故障抢修", "日常小修", "计划大修")
STATUS = ("优", "良", "中", "差")
