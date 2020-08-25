# -*- coding: utf-8 -*-

from productline.models.productlinemodel import ProductLineModel
from product.controllers.productcontroller import ProductController

class ProductLineConroller(object):
    def __init__(self):
        self.PC = ProductController()

    def get_productline(self, autoid=None, pltype=None):
        kwarg = dict()
        if autoid:
            kwarg['autoid'] = autoid
        if pltype is not None:
            kwarg['pltype'] = pltype
        if kwarg:
            return ProductLineModel.get_productline(**kwarg)
        else:
            return False

    def get_workflow(self, plid, *args, **kwargs):
        return ProductLineModel.get_workflow(plid, *args, **kwargs)

    def get_formula(self, *args, **kwargs):
        return ProductLineModel.get_formula(*args, **kwargs)

    def get_product_detail(self,flag=0, *args, **kwargs):
        return self.PC.get_producingplan(flag, *args, **kwargs)