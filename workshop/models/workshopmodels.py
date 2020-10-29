# -*- coding: utf-8 -*-
from lib.utils.saveexcept import SaveExcept
from django.db import transaction, connection
from db.models import Productdictionary, Plids, Producingplan, Linepost, \
    Linepostdocument, Forms, Selfdefinedformat, Productputinnotes, Prodqrcode, \
    Qrcoderepository


class WorkshopModels(object):

    def get_linepost(self, ppid):
        return Linepost.objects.filter(ppid=ppid).order_by('seqid')

    def get_linepostdocuments(self, lpid):
        return Linepostdocument.objects.filter(lpid__in=lpid).order_by('lpid', 'seqid')

    def get_form(self, aid):
        return Forms.objects.get(autoid=aid)

    def update_form(self, aid: int, content):
        return Forms.objects.filter(autoid=aid).update(format=content)

    def reset_form(self, aid: int):
        res = Forms.objects.get(autoid=aid)
        if res is not None:
            ori_content = Selfdefinedformat.object.get(autoid=res.selfid)

        return Forms.objects.filter(autoid=aid).update(format=ori_content)

    @staticmethod
    def get_productputinnote(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Productputinnotes.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取产品入库信息时出错", *args,
                       **kwargs)

    @staticmethod
    def get_prodqrcode(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Prodqrcode.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取产品二维码时出错", *args,
                       **kwargs)

    @staticmethod
    def get_plids(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Plids.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取批记录图片时出错", *args, **kwargs)

    @staticmethod
    def get_qrcoderep(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Prodqrcode.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取二维码库时出错", *args,
                       **kwargs)

    @staticmethod
    def update_productputinnote(autoid, *args, **kwargs):
        if type(autoid) is int:
            return Productputinnotes.objects.filter(autoid=autoid).update(**kwargs)
        elif type(autoid) is list:
            return Productputinnotes.objects.filter(autoid__in=autoid).update(**kwargs)
        else:
            return Productputinnotes.objects.create(**kwargs)

    @staticmethod
    def update_prodqrcode(key_dict=None, *args, **kwargs):
        if key_dict:
            return Prodqrcode.objects.filter(**key_dict).update(**kwargs)
        else:
            return Prodqrcode.objects.create(**kwargs)

    @staticmethod
    def delete_prodqrcode(*args, **kwargs):
        return Productputinnotes.objects.filter(**kwargs).delete()