# -*- coding: utf-8 -*-

from lib.utils.saveexcept import SaveExcept

from db.models import Labrecords, Labrecordsdetail, Originalcheckpaper, \
    Originalcheckpapersetting, Checkitems

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
    def delete_labrecord(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Labrecords.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Labrecords.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Labrecords.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除检验记录时出错", *args, *kwargs)

    @staticmethod
    def update_labitem(autoid=0, *args, **kwargs):
        if autoid:
            return Labrecordsdetail.objects.filter(autoid=autoid).update(
                **kwargs)
        else:
            return Labrecordsdetail.objects.create(**kwargs)

    @staticmethod
    def delete_labitem(autoid=None, *args, **kwargs):
        try:
            if autoid is not None:
                if type(autoid) == int:
                    return Labrecordsdetail.objects.filter(
                        autoid=autoid).delete()
                elif type(autoid) == list:
                    return Labrecordsdetail.objects.filter(
                        autoid__in=autoid).delete()
            elif len(kwargs):
                return Labrecordsdetail.objects.filter(**kwargs).delete()
            else:
                return False
        except Exception as e:
            SaveExcept(e, "删除检验项目时出错", *args, *kwargs)

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


    @staticmethod
    def get_data(table_str, err_msg=None, display_flag=False, *args, **kwargs):
        try:
            table = globals()[table_str]
        except KeyError:
            return False
        flat = True if len(args) == 1 else False
        try:
            res = table.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, err_msg, *args, **kwargs)

    @staticmethod
    def update_data(table_str, err_msg=None, condition={}, *args, **kwargs):
        try:
            table = globals()[table_str]
        except KeyError:
            return False
        try:
            if len(args):
                return table.objects.filter(autoid__in=args).update(**kwargs)
            elif len(condition):
                return table.objects.filter(**condition).update(**kwargs)
            else:
                return table.objects.create(**kwargs)
        except Exception as e:
            SaveExcept(e, err_msg, *args, **kwargs)

    @staticmethod
    def delete_data(table_str, err_msg=None, condition={}, *args, **kwargs):
        try:
            table = globals()[table_str]
        except KeyError:
            return False
        try:
            if len(args):
                return table.objects.filter(autoid__in=args).delete()
            elif len(condition):
                return table.objects.filter(**condition).delete()
            else:
                return table.objects.filter(**kwargs).delete()
        except Exception as e:
            SaveExcept(e, err_msg, *args, **kwargs)
