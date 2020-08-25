# -*- coding: utf-8 -*-

from db.models import Cleanconfirmity


class CleanfirmityModels(object):
    #def __init__(self):
    #self.CM = Cleanconfirmity()

    @staticmethod
    def get_cleanfirmity(autoid=0, *args, **kwargs):
        if autoid:
            kwargs.update(autoid=autoid)
        if args:
            return Cleanconfirmity.objects.filter(**kwargs).values_list(*args)
        else:
            return Cleanconfirmity.objects.filter(**kwargs)

    @staticmethod
    def update_cleanfirmity(condition: dict, *args, **kwargs):
        if condition:
            return Cleanconfirmity.objects.filter(**condition).update(**kwargs)
        else:
            return Cleanconfirmity.objects.create(**kwargs)
