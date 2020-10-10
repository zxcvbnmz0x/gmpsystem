# -*- coding: utf-8 -*-

from system.models.systemmodel import SystemModel


class SystemController():

    def get_systemoption(self, flag=False, *args, **kwargs):
        return SystemModel.get_systemoption(flag, *args, **kwargs)

    def update_systemoption(self, otid, *args, **kwargs):
        return SystemModel.update_systemoption(otid, *args, **kwargs)

    def delete_systemoption(self, otid, *args, **kwargs):
        return SystemModel.delete_systemoption(otid, *args, **kwargs)

    def get_syssetting(self, flag=False, *args, **kwargs):
        return SystemModel.get_syssetting(flag, *args, **kwargs)

    def update_syssetting(self, otid, *args, **kwargs):
        return SystemModel.update_syssetting(otid, *args, **kwargs)

    def delete_Syssetting(self, otid, *args, **kwargs):
        return SystemModel.delete_Syssetting(otid, *args, **kwargs)
