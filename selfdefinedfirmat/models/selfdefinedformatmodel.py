# -*- coding: utf-8 -*-

from db.models import Selfdefinedformat

from lib.utils.saveexcept import SaveExcept


class SelfdefinedformatModel():

    @staticmethod
    def get_selfdefinedformat(flag=False, *args, **kwargs):
        try:
            flat = True if len(args) == 1 else False
            res = Selfdefinedformat.objects.filter(**kwargs)
            if len(args):
                if flag:
                    return res.values_list(*args, flat=flat)
                else:
                    return res.values(*args)
            else:
                return res
        except Exception as e:
            SaveExcept(e, "获取自定义文档时出错", *args, **kwargs)

    @staticmethod
    def update_selfdefinedformat(autoid=0, *args, **kwargs):
        if autoid:
            return Selfdefinedformat.objects.filter(autoid=autoid).update(
                **kwargs)
        else:
            return Selfdefinedformat.objects.create(**kwargs)
