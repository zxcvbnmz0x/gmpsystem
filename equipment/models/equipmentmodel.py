# -*- coding: utf-8 -*-

from db.models import Equipments, Eqrunnotes
from django.db import transaction

class EquipmentModel(object):

    @staticmethod
    def get_equip_run_note(autoid=0, olist=[], *args, **kwargs):
        if autoid:
            kwargs.update(autoid=autoid)
        flat = True if len(args) == 1 else False
        res = Eqrunnotes.objects.filter(**kwargs)
        if len(olist):
            res = res.order_by(*olist)
        if len(args):
            return res.values_list(*args, flat=flat)
        else:
            return res

    @staticmethod
    def get_equipment(autoid=0, olist=[], *args, **kwargs):
        if autoid:
            kwargs.update(autoid=autoid)
        flat = True if len(args) == 1 else False
        res = Equipments.objects.filter(**kwargs)
        if len(olist):
            res = res.order_by(*olist)
        if len(args):
            return res.values_list(*args, flat=flat)
        else:
            return res

    @staticmethod
    def delete_equip_run_note(autoid, *args, **kwargs):
        if autoid:
            kwargs.update(autoid__in=autoid)
        return Eqrunnotes.objects.filter(**kwargs).delete()

    @staticmethod
    def insert_equip_run_note(autoid, *args, **kwargs):
        colums_list = ('eqno', 'runstarttime', 'batchno', 'dictid', 'dictname', 'pid', 'rtype','postname', 'lpid', 'runendtime')
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