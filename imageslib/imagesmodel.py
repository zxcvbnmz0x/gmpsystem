# -*- coding: utf-8 -*-

from db.models import Relativepictures, Imagelib

from lib.utils.saveexcept import SaveExcept
from django.db import transaction


class ImagesModel():
    def __init__(self):
        rela_detail = []

    @staticmethod
    def get_rela(flag=False, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Relativepictures.objects.filter(**kwargs)
            if len(args):
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取图片关系出错", *args, **kwargs) \
 \
            @ staticmethod

    def get_img(flag=False, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Imagelib.objects.filter(**kwargs)
            if len(args):
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取图片出错", *args, **kwargs)
    #
    # @staticmethod
    # def update_rela(autoid=0, *args, **kwargs):
    #     if autoid:
    #         return Relativepictures.objects.filter(autoid=autoid).update(
    #             **kwargs)
    #     else:
    #         return Relativepictures.objects.create(**kwargs)
    #     try:
    #         pass
    #     except Exception as e:
    #         SaveExcept(e, "更新图片关系出错", autoid, *args, **kwargs)

    @staticmethod
    def update_img(relakwargs, imgkwargs, relaid=0, imgid=0):
        if (relaid and not imgid) or (not relaid and imgid):
            return []

        try:
            with transaction.atomic():
                p1 = transaction.savepoint()
                if relaid:
                    res_rela = Relativepictures.objects.filter(
                        autoid=relaid).update(**relakwargs)
                    res_img = Imagelib.objects.filter(autoid=imgid).update(
                        **imgkwargs)
                else:
                    res_img = Imagelib.objects.create(**imgkwargs)
                    relakwargs.update({'imageid': res_img.autoid})
                    res_rela = Relativepictures.objects.create(**relakwargs)
                if res_img and res_rela:
                    transaction.savepoint()
                    return "accept"
                else:
                    transaction.savepoint_rollback(p1)
                    return "roolback"
        except Exception as e:
            SaveExcept(e, "更新图片时出错", data=(relaid, imgid),
                       relakwargs=relakwargs, imgkwargs=imgkwargs)

    @staticmethod
    def delete_img(relaid, imgid):
        if (relaid and not imgid) or (not relaid and imgid):
            return []
        try:
            with transaction.atomic():
                p1 = transaction.savepoint()
                res_rela = Relativepictures.objects.filter(
                    autoid__in=relaid).delete()
                res_img = Imagelib.objects.filter(autoid__in=imgid).delete()

                if res_img and res_rela:
                    transaction.savepoint()
                    return "accept"
                else:
                    transaction.savepoint_rollback(p1)
                    return "roolback"
        except Exception as e:
            SaveExcept(e, "删除图片时出错", data=(relaid, imgid))

