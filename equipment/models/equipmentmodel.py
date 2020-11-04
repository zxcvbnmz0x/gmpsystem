# -*- coding: utf-8 -*-

from db.models import Equipments, Eqrunnotes, Eqcheck, Eqrepairnotes, \
    Eqaccidentnotes, Eqnormaldocuments
from django.db import transaction
from lib.utils.saveexcept import SaveExcept


class EquipmentModel(object):

    @staticmethod
    def get_equip_run_note(autoid=0, olist=[], *args, **kwargs):
        if autoid:
            Eqrunnotes.filter(autoid=autoid)
        flat = True if len(args) == 1 else False
        res = Eqrunnotes.objects.filter(**kwargs)
        if len(olist):
            res = res.order_by(*olist)
        if len(args):
            return res.values_list(*args, flat=flat)
        else:
            return res

    @staticmethod
    def get_equipment(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Equipments.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取设备信息时出错", *args, **kwargs)

    @staticmethod
    def delete_equip_run_note(autoid, *args, **kwargs):
        if autoid:
            kwargs.update(autoid__in=autoid)
        return Eqrunnotes.objects.filter(**kwargs).delete()

    @staticmethod
    def insert_equip_run_note(autoid, *args, **kwargs):
        colums_list = (
            'eqno', 'runstarttime', 'batchno', 'dictid', 'dictname', 'pid',
            'rtype','postname', 'lpid', 'runendtime', 'status'
        )
        if autoid:
            kwargs.update(autoid__in=autoid)
        records = Eqrunnotes.objects.filter(**kwargs).values(*colums_list)
        res_list = []
        with transaction.atomic():
            for item in records:
                print(item)
                res =Eqrunnotes.objects.create(**item)
                res_list.append(res)
        return res_list

    @staticmethod
    def update_equip_run_note(autoid, *args, **kwargs):
        if autoid:
            return Eqrunnotes.objects.filter(autoid=autoid).update(**kwargs)
        else:
            return Eqrunnotes.objects.create(**kwargs)

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
