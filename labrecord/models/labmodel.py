# -*- coding: utf-8 -*-

from lib.utils.saveexcept import SaveExcept

from db.models import Labrecords, Labrecordsdetail, Originalcheckpaper


class LabModel(object):
    def __init__(self):
        super().__init__()

    @staticmethod
    def get_labrecord(flag=0, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Labrecords.objects.filter(**kwargs)
            if len(args):
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取检验记录时出错", *args, **kwargs)

    @staticmethod
    def get_labitem(flag=0, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Labrecordsdetail.objects.filter(**kwargs)
            if len(args):
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取检验项目时出错", *args, **kwargs)
