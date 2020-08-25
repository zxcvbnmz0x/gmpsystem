# -*- coding: utf-8 -*-


# 用于递归循环时抛出异常
class TailRecurseException(BaseException):
    def __init__(self, args, kwargs):
        self.args = args
        self.kwargs = kwargs
