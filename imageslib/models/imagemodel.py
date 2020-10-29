# -*- coding: utf-8 -*-

from db.models import Imagelib

from lib.utils.saveexcept import SaveExcept

class Imagemodel(object):

    @staticmethod
    def get_image(display_flag=False, *args, **kwargs):
        flat = True if len(args) == 1 else False
        try:
            res = Imagelib.objects.filter(**kwargs)
            if len(args):
                if display_flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取图片库时出错", *args, **kwargs)

    @staticmethod
    def delete_image(*args, **kwargs):
        return Imagelib.objects.filter(**kwargs).delete()

    @staticmethod
    def save_image(key_dict=None, *args, **kwargs):
        if key_dict:
            return Imagelib.objects.filter(**key_dict).update(**kwargs)
        else:
            return Imagelib.objects.create(**kwargs)
