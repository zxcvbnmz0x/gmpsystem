# -*- coding: utf-8 -*-

from lib.utils.saveexcept import SaveExcept

from db.models import Labrecords, Labrecordsdetail, Originalcheckpaper, \
    Originalcheckpapersetting

from django.db import connection

class LabModel(object):

    @staticmethod
    def get_labrecord(flag=False, *args, **kwargs):
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
    def get_labitem(flag=False, *args, **kwargs):
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

    @staticmethod
    def get_oricheckpapersetting(flag=False, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Originalcheckpapersetting.objects.filter(**kwargs)
            if len(args):
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取原始检验记录设置时出错", *args, **kwargs)

    @staticmethod
    def get_oricheckpaper(flag=False, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Originalcheckpaper.objects.filter(**kwargs)
            if len(args):
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取原始检验记录时出错", *args, **kwargs)

    @staticmethod
    def get_paperno(lrid):
        cursor = connection.cursor()
        cursor.execute("select GenLabPaperNo(%s)" % lrid)
        raw = cursor.fetchone()
        return raw

    @staticmethod
    def update_labrecord(autoid=0, *args, **kwargs):
        if autoid:
            return Labrecords.objects.filter(autoid=autoid).update(**kwargs)
        else:
            return Labrecords.objects.create(**kwargs)

    @staticmethod
    def update_labitem(autoid=0, *args, **kwargs):
        if autoid:
            return Labrecordsdetail.objects.filter(autoid=autoid).update(
                **kwargs)
        else:
            return Labrecordsdetail.objects.create(**kwargs)

    @staticmethod
    def update_oricheckpaper(autoid=0, *args, **kwargs):
        if autoid:
            return Originalcheckpaper.objects.filter(autoid=autoid).update(
                **kwargs)
        else:
            return Originalcheckpaper.objects.create(**kwargs)

    @staticmethod
    def delete_oricheckpaper(id_list):
        return Originalcheckpaper.objects.filter(autoid__in=id_list).delete()