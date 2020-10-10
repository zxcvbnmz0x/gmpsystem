# -*- coding: utf-8 -*-

from selfdefinedfirmat.models.selfdefinedformatmodel import SelfdefinedformatModel


class SelfdefinedformatController():

    def get_selfdefinedformat(self, flag, *args, **kwargs):
        return SelfdefinedformatModel.get_selfdefinedformat(flag, *args, **kwargs)

    @staticmethod
    def update_selfdefinedformat(autoid=0, *args, **kwargs):
        return SelfdefinedformatModel.update_selfdefinedformat(autoid, *args, **kwargs)
