# -*- coding: utf-8 -*-
import datetime
from PyQt5.QtCore import QTimer

user_id = "001"
user_name = "sys02"
dept_id = "002"
dept_name = "生产部"
now_date = datetime.date.today()
time = datetime.datetime.now()
now_time = time.strftime('%Y-%m-%d %H:%M')
NIAN = time.strftime("%Y")
YUE = time.strftime("%m")
RI = time.strftime("%d")
SHI = time.strftime("%H")
FEN = time.strftime("%M")
MIAO = time.strftime("%S")

unsigndate = datetime.date.min
unsigntime = datetime.time.min
unsigndatetime = datetime.datetime.min


def currentdatetime():
    return datetime.datetime.now()