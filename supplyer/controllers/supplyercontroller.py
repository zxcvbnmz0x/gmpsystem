# -*- coding: utf-8 -*-

from supplyer.models.supplyermodel import SupplyerModel


class SupplyerController(object):
    def __init__(self):
        pass

    def get_supply(self, flag=0, *args,  **kwargs):
        return SupplyerModel.get_supply(flag=0, *args, **kwargs)
