# -*- coding: utf-8 -*-

from supplyer.models.supplyermodel import SupplyerModel


class SupplyerController(object):

    def get_supply(self, display_flag=False, *args,  **kwargs):
        return SupplyerModel.get_supply(display_flag, *args, **kwargs)

    def get_purchasingplan(self, display_flag=False, *args, **kwargs):
        return SupplyerModel.get_purchasingplan(display_flag, *args, **kwargs)

    def update_purchasingplan(self, autoid=None, *args, **kwargs):
        return SupplyerModel.update_purchasingplan(autoid, *args, **kwargs)

    def delete_purchasingplan(self, autoid, *args, **kwargs):
        return SupplyerModel.delete_ppurchasingplan(autoid, *args, **kwargs)

    def get_purchstuff(self, display_flag=False, *args, **kwargs):
        return SupplyerModel.get_purchstuff(display_flag, *args, **kwargs)

    def update_purchstuff(self, autoid, *args, **kwargs):
        return SupplyerModel.update_purchstuff(autoid, *args, **kwargs)

    def delete_purchstuff(self, autoid=None, *args, **kwargs):
        return SupplyerModel.delete_purchstuff(autoid, *args, **kwargs)

    def get_stuffsupplyer(self, display_flag=False, *args, **kwargs):
        return SupplyerModel.get_stuffsupplyer(display_flag, *args, **kwargs)
