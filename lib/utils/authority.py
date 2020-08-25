import traceback

from db.models import Clerks
from django.db import utils


class Authority(object):
    def __init__(self):
        super().__init__()

    # 获得所有人员信息
    def get_authoriy(self, clerkid):
        try:
            return Clerks.objects.values_list('powers',flat=True).filter(clerkid=clerkid)
        except Exception as e:
            print("插入部门发生错误")
            # 这个是输出错误的具体原因，这步可以不用加str，输出
            print("这里是错误的具体原因")
            # 输出 repr(e):	ZeroDivisionError('integer division or modulo by zero',)
            print('repr(e):\t', repr(e))
            # 以下两步都是输出错误的具体位置的
            print('traceback.print_exc():')
            traceback.print_exc()