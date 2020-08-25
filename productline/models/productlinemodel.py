# -*- coding: utf-8 -*-

from db.models import Productline, Workflow, Productprescription


class ProductLineModel(object):

    @staticmethod
    def get_productline(**kwargs):
        return Productline.objects.filter(**kwargs)

    @staticmethod
    def get_workflow(plid=0, *args, **kwargs):
        flat = True if len(args) == 1 else False
        if plid:
            kwargs.update(plid=plid)
        if len(args):
            return Workflow.objects.filter(**kwargs).values_list(*args, flat=flat)
        else:
            return Workflow.objects.filter(**kwargs)

    @staticmethod
    def get_formula(*args, **kwargs):
        flat = True if len(args) == 1 else False
        if len(args):
            return Productprescription.objects.filter(**kwargs).values_list(*args,
                                                                 flat=flat)
        else:
            return Productprescription.objects.filter(**kwargs)
